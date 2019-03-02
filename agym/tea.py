"""
    Core library module.

    Classes:
        Tea - core logic class, provides functions for task,
        supertask, user, etc.

    For more information, see help(Tea)
"""
from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.query import Query
from queue import Queue
from datetime import datetime, timedelta
from tzlocal import get_localzone

from tea.models import (
    Base,
    User,
    Task,
    SuperTask,
    Tag,
    Comment,
    Notification,
    SuperTaskKind,
    NotificationKind,
    TaskPriority
)

from tea.exceptions import (
    EntityDontExistsError,
    ObjectDontExistsError,
    CicleDependenceError,
)
from tea.logger_utils import get_logger

from typing import (
    List,
    Any,
    NewType,
    Tuple,
    Mapping
)

Datetime = NewType("Datetime", datetime)
Timedelta = NewType("Timedelta", timedelta)

NUM_LETTER_FROM_DESCRIPTION_TO_TITLE = 20


class Tea:
    """Core library class, provides functions for task, supertask, user, tag, comment, notification.

    Usage examples:
        Task manager creation::
            >>> from tea import Tea
            >>> from datetime import datetime
            >>> tea = Tea(db_string="postgres://anton:12345678@localhost/tea_db")

        Task creation::
            >>> dateformat = "%d/%m/%Y %H:%M"
            >>> deadline = datetime.strptime("1999/10/18 14:20", dateformat)
            >>> task_id = tea.add_task(description="Buy socks", deadline=deadline)

        Adding user permissions to task::
            >>> tea.add_doer(user_id=user_id, task_id=task_id)

        Working with notifications::
            >>> notification_id = tea.add_notification(text=text, user_id=user_id)
            >>> notification = tea.get_object("notification", notification_id)
            >>> print(notification.is_seen)
            False
            >>> tea.edit_notification(id=notification_id, is_seen=True)
            >>> print(notification.is_seen)
            True

        Getting object connecting to someting::
            >>> tasks = tea.get_tasks(user_ids=[1, 2], tag_ids=[3, 34])

        Getting users or tags by name::
            >>> users = tea.get_users(names=["seagull", "studpy"])
    """

    def __init__(self, db_string: str):
        """
            Args:
                db_string: string to connect to database
        """

        self.str_to_model_mapper = {
            "user": User,
            "task": Task,
            "supertask": SuperTask,
            "tag": Tag,
            "comment": Comment,
            "notification": Notification,
        }

        self.db_engine = create_engine(db_string)
        Base.metadata.create_all(self.db_engine)

        self.session = sessionmaker(self.db_engine)()

    def clear(self):
        """
            Clear all tables in db through droping and re_creation.
        """
        Base.metadata.drop_all(self.db_engine)
        Base.metadata.create_all(self.db_engine)

    def __del__(self):
        if self.session is not None:
            self.session.close()

    # region adding
    def add_user(self,
                 name: str,
                 creation_time: Datetime = None,
                 email: str = None) -> int:
        """Add new user with passed params and return it's id."""
        get_logger().info("Received request for adding users.")
        if creation_time is None:
            creation_time = get_localzone().localize(datetime.now())

        user = User(
            name=name,
            creation_time=creation_time,
            email=email,
        )

        self.session.add(user)
        self.session.commit()

        return user.id

    def add_task(self,
                 description: str,
                 deadline: Datetime,
                 priority: TaskPriority = TaskPriority.MEDIUM,
                 title: str = None,
                 creation_time: Datetime = None) -> int:
        """Add new task with passed params and return it's id."""
        get_logger().info("Received request for adding tasks.")
        if creation_time is None:
            creation_time = get_localzone().localize(datetime.now())
        if title is None:
            title = description[:NUM_LETTER_FROM_DESCRIPTION_TO_TITLE]
        if priority is None:
            priority = TaskPriority.MEDIUM

        task = Task(
            title=title,
            description=description,
            deadline=deadline,
            creation_time=creation_time,
            execution_time=None,
            is_done=False,
            is_expired=False,
            is_archived=False,
            priority=priority,
        )

        self.session.add(task)
        self.session.commit()

        return task.id

    def add_supertask(self,
                      creator_id: int,
                      description: str,
                      kind: SuperTaskKind,
                      first_creation_time: Datetime,
                      re_creation_period: Timedelta = None,
                      title: str = None,
                      week_mask: str = None,
                      time_to_execution: Timedelta = None,
                      priority: TaskPriority = TaskPriority.MEDIUM,
                      creation_time: Datetime = None) -> int:
        """
        Add new supertask with passed params and return it's id.

        Args:
            creator_id: id of creator user
            description: description for created tasks
            kind: kind of supertask, maybe Interval or Week
            first_creation_time: time when first task will be created;
            all tasks from Week supertask will be created in first_creation_time;
            re_creation_period: period between creation tasks. Matter only for Interval supertask.
            end_creation_time: datetime, when tasks stop creation
            title: title for created tasks. If is None take first letter of description
            week_mask: string from 7 char of {0, 1}, 1 on i-th position means that task will be created on day i of week
            time_to_execution: period when task may be done, default: re_creation_period
            creation_time: datetime for explicit passing time for creation supertask 
        """
        get_logger().info("Received request for adding supertasks.")
        if creation_time is None:
            creation_time = get_localzone().localize(datetime.now())
        if time_to_execution is None:
            time_to_execution = re_creation_period
        if title is None:
            title = description[:NUM_LETTER_FROM_DESCRIPTION_TO_TITLE]

        supertask = SuperTask(
            creator_id=creator_id,
            kind=kind,
            title=title,
            description=description,
            creation_time=creation_time,
            time_to_execution=time_to_execution,
            next_creation_time=first_creation_time,
            re_creation_period=re_creation_period,
            priority=priority,
            week_mask=week_mask,
        )

        self.session.add(supertask)
        self.session.commit()

        return supertask.id

    def add_tag(self,
                name: str,
                creation_time: Datetime = None) -> int:
        """Add new tag with passed params and return it's id."""
        get_logger().info("Received request for adding tags.")
        if creation_time is None:
            creation_time = get_localzone().localize(datetime.now())

        tag = Tag(
            name=name,
            creation_time=creation_time,
        )

        self.session.add(tag)
        self.session.commit()

        return tag.id

    def add_comment(self,
                    text: str,
                    user_id: int,
                    task_id: int,
                    creation_time: Datetime = None) -> int:
        """
        Add new comment with passed params and return it's id.

        Args:
            text: text of comment
            user_id: owner of comment, which will be auto-connected with comment 
            task_id: task, where comment will be displayed
            creation_time: datetime for explicit passing time for creation comment

        """
        get_logger().info("Received request for adding comments.")
        if creation_time is None:
            creation_time = get_localzone().localize(datetime.now())

        comment = Comment(
            text=text,
            creation_time=creation_time,
            owner_id=user_id,
            task_id=task_id,
        )

        self.session.add(comment)
        self.session.commit()

        return comment.id

    def add_notification(self,
                         notification_kind: NotificationKind,
                         description: str,
                         user_id: int,
                         creation_time: Datetime = None) -> int:
        """
        Add new notification with passed params and return it's id.

        Args:
            notification_kind: kind of notification from tea.models.notification
            description: text, what will be display
            user_id: target user to whom notification applies
        """
        get_logger().info("Received request for adding notifications.")
        if creation_time is None:
            creation_time = get_localzone().localize(datetime.now())

        notification = Notification(
            is_seen=False,
            kind=notification_kind,
            description=description,
            creation_time=creation_time,
            user_id=user_id,
        )

        self.session.add(notification)
        self.session.commit()

        return notification.id
    # endregion

    # region editing
    def edit_user(self,
                  id: int,
                  name: str = None,
                  email: str = None):
        """
            Change not None passed fields for user

            Args:
                id: id of user
                name: new name of user
                email: new email of user
        """
        get_logger().info("Received request for editing users.")
        self._edit_object(
            model=User,
            id=id,
            name=name,
            email=email,
        )

    def edit_task(self,
                  id: int,
                  title: str = None,
                  deadline: Datetime = None,
                  description: str = None,
                  priority: TaskPriority = None,
                  is_archived: bool = None):
        """
            Change not None passed fields for task

            Args:
                id: id of task
                title: new title of task
                priority: new priority of task
                deadline: new deadline of task
                description: new description of task
                is_archived: new archive status of task
        """
        get_logger().info("Received request for editing tasks.")

        editing_time = get_localzone().localize(datetime.now())

        self._edit_object(
            model=Task,
            id=id,
            title=title,
            priority=priority,
            deadline=deadline,
            description=description,
            is_archived=is_archived,
            last_editing_time=editing_time,
        )

    def edit_supertask(self,
                       id: int,
                       title: str = None,
                       description: str = None,
                       week_mask: str = None,
                       kind: SuperTaskKind = None,
                       priority: TaskPriority = None,
                       next_creation_time: Datetime = None,
                       time_to_execution: Timedelta = None,
                       re_creation_period: Timedelta = None):
        """
            Change not None passed fields for supertask. For meaning all
            variable see docstring of Tea.add_supertask.

            Args:
                id: id of supertask
                title: new title for created task
                description: new description for created task
                week_mask: new week_mask of supertask
                kind: new kind of supertask
                next_creation_time: new next_creation_time of supertask
                time_to_execution: new time_to_execution for created task
                re_creation_period: new re_creation_period of supertask
        """
        get_logger().info("Received request for editing supertasks.")

        editing_time = get_localzone().localize(datetime.now())

        self._edit_object(
            model=SuperTask,
            id=id,
            title=title,
            description=description,
            week_mask=week_mask,
            kind=kind,
            priority=priority,
            next_creation_time=next_creation_time,
            time_to_execution=time_to_execution,
            re_creation_period=re_creation_period,
            last_editing_time=editing_time,
        )

    def edit_tag(self,
                 id: int,
                 name: str = None):
        """
            Change not None passed fields for tag

            Args:
                id: id of tag
                name: new name of tag
        """
        get_logger().info("Received request for editing tags.")
        self._edit_object(
            model=Tag,
            id=id,
            name=name,
        )

    def edit_comment(self,
                     id: int,
                     text: str = None):
        """
            Change not None passed fields for comment

            Args:
                id: id of comment
                text: new text of comment
        """
        get_logger().info("Received request for editing comments.")
        self._edit_object(
            model=Comment,
            id=id,
            text=text,
        )

    def edit_notification(self,
                          id: int,
                          is_seen: bool = None,
                          kind: NotificationKind = None,
                          description: str = None):
        """
            Change not None passed fields for comment. For meaming of
            variables see docstring of Tea.add_notification.

            Args:
                id: id of notification
                is_seen: new status of seing of notification
                kind: new kind of notification
                description: new description of notification
        """
        get_logger().info("Received request for editing notifications.")
        self._edit_object(
            model=Notification,
            id=id,
            is_seen=is_seen,
            kind=kind,
            description=description,
        )

    def _edit_object(self,
                     model: Any,
                     id: int,
                     **editting_fields_dict: Mapping[str, Any]):
        """
            Private method for implementation of Tea.edit_*.
            If item.value of item from editting_fields_dict isn't None and
            'model' has attribute item.key, get object of 'model' with id
            equal 'id' and set attribute of object with name item.key to
            item.value.

            Args:
                model: type of entity
                id: id of entity
                **editting_fields_dict: dict
        """
        instance = self._get_object(model, id)

        for fieldname, new_value in editting_fields_dict.agym.items():
            if not hasattr(instance, fieldname):
                raise ValueError(
                    "Instance of {} hasn't field with name {}".format(
                        model.__name__,
                        fieldname,
                    )
                )

            if new_value is not None:
                setattr(instance, fieldname, new_value)

        self.session.commit()
    # endregion

    # region getting
    def get_users(self,
                  user_ids: List[int] = None,
                  task_ids: List[int] = None,
                  supertask_ids: List[int] = None,
                  names: List[str] = None) -> List[User]:
        """
            Return list of users with passed params.

            Result will be conjunctions(through params) of
            disjunctions(through id of id-params). So this method
            return obj, which must be in user_ids, and connect with
            at least one task from task_ids and atleast one supertask from
            supertask_ids if ids is not None.

            Args:
                user_ids: list of user ids which are permmited to return
                task_ids: list of task ids which must be connected
                supertask_ids: list of supertask ids which must be connected
        """
        get_logger().info("Received request for getting users.")

        # for understanding this variable, see Tea._get_objects docstring
        join_infos = [
            (Task, User.tasks_as_doer, task_ids),
            (SuperTask, User.supertasks_as_doer, supertask_ids)
        ]

        query = self._get_objects(
            model=User,
            join_infos=join_infos,
        )

        if user_ids is not None:
            query = query.filter(User.id.in_(user_ids))
        if names is not None:
            query = query.filter(User.name.in_(names))

        result_objects = query.all()

        get_logger().debug("Request of getting users is performed."
                           " Returned {} users.".format(len(result_objects)))
        return result_objects

    def get_tasks(self,
                  task_ids: List[int] = None,
                  user_ids: List[int] = None,
                  tag_ids: List[int] = None) -> List[Task]:
        """
            Return list of tasks with passed params.

            Result will be conjunctions(through params) of
            disjunctions(through id of id-params). So this method
            return obj, which must be in task_ids, and connect with
            at least one user from user_ids and at least one tag from
            tag_ids if ids is not None.

            Args:
                task_ids: list of task which are permmited to return
                user_ids: list of user which must be connected
                tag_ids: list of tag which must be connected
        """
        get_logger().info("Received request for getting tasks.")

        query = self.session.query(Task)

        if user_ids is not None:
            query = query.filter(
                or_(
                    Task.creator_id.in_(user_ids),
                    Task.moderators.any(User.id.in_(user_ids)),
                    Task.doers.any(User.id.in_(user_ids)),
                    Task.watchers.any(User.id.in_(user_ids))
                )
            )

        if task_ids is not None:
            query = query.filter(Task.id.in_(task_ids))

        if tag_ids is not None:
            query = query.filter(Task.tags.any(Tag.id.in_(tag_ids)))

        result_objects = query.all()

        get_logger().debug("Request of getting tasks is performed."
                           " Returned {} tasks.".format(len(result_objects)))
        return result_objects

    def get_supertasks(self,
                       supertask_ids: List[int] = None,
                       user_ids: List[int] = None,
                       tag_ids: List[int] = None) -> List[SuperTask]:
        """
            Return list of supertasks with passed params.

            Result will be conjunctions(through params) of
            disjunctions(through id of id-params). So this method
            return obj, which must be in supertask_ids, and connect with
            at least one user from user_ids and at least one tag from
            tag_ids if ids is not None.

            Args:
                supertask_ids: list of supertask which are permmited to return
                user_ids: list of user which must be connected
                tag_ids: list of tag which must be connected
        """
        get_logger().info("Received request for getting supertasks.")

        query = self.session.query(SuperTask)

        if user_ids is not None:
            query = query.filter(
                or_(
                    SuperTask.creator_id.in_(user_ids),
                    SuperTask.moderators.any(User.id.in_(user_ids)),
                    SuperTask.doers.any(User.id.in_(user_ids)),
                    SuperTask.watchers.any(User.id.in_(user_ids))
                )
            )

        if supertask_ids is not None:
            query = query.filter(SuperTask.id.in_(supertask_ids))

        if tag_ids is not None:
            query = query.filter(SuperTask.tags.any(Tag.id.in_(tag_ids)))

        result_objects = query.all()

        get_logger().debug(
            "Request of getting supertasks is performed."
            " Returned {} supertasks.".format(
                len(result_objects)
            )
        )
        return result_objects

    def get_tags(self,
                 tag_ids: List[int] = None,
                 task_ids: List[int] = None,
                 supertask_ids: List[int] = None,
                 names: List[str] = None) -> List[Tag]:
        """
            Return list of tags with passed params.

            Result will be conjunctions(through params) of
            disjunctions(through id of id-params). So this method
            return obj, which must be in tag_ids, and connect with
            atleast one task from task_ids and atleast one supertaks from
            supertask_ids if ids is not None.

            Args:
                tag_ids: list of tag which are permmited to return
                task_ids: list of task which must be connected
                supertask_ids: list of supertask which must be connected
        """
        get_logger().info("Received request for getting tags.")

        # for understanding this variable, see Tea._get_objects docstring
        join_infos = [
            (Task, Tag.tasks, task_ids),
            (SuperTask, Tag.supertasks, supertask_ids)
        ]

        query = self._get_objects(
            model=Tag,
            join_infos=join_infos,
        )

        if tag_ids is not None:
            query = query.filter(Tag.id.in_(tag_ids))
        if names is not None:
            query = query.filter(Tag.name.in_(names))

        result_objects = query.all()

        get_logger().debug(
            "Request of getting tags is performed."
            " Returned {} tags.".format(
                len(result_objects)
            )
        )
        return result_objects

    def get_comments(self,
                     comment_ids: List[int] = None,
                     user_ids: List[int] = None,
                     task_ids: List[int] = None) -> List[Comment]:
        """
            Return list of users with passed params.

            Result will be conjunctions(through params) of
            disjunctions(through id of id-params). So this method
            return obj, which must be in comment_ids, and connect with
            at least one task from task_ids and atleast one user from
            user_ids if ids is not None.

            Args:
                comment_ids: list of comment which are permmited to return
                user_ids: list of user which must be connected
                task_ids: list of task which must be connected
        """
        get_logger().info("Received request for getting comments.")

        join_infos = [
            (User, Comment.owner, user_ids),
            (Task, Comment.task, task_ids),
        ]

        # for understanding this variable, see Tea._get_objects docstring
        query = self._get_objects(
            model=Comment,
            join_infos=join_infos,
        )

        if comment_ids is not None:
            query = query.filter(Comment.id.in_(comment_ids))

        result_objects = query.all()

        get_logger().debug("Request of getting tags is performed."
                           " Returned {} tags.".format(len(result_objects)))
        return result_objects

    def get_notifications(self,
                          notification_ids: List[int] = None,
                          user_ids: List[int] = None) -> List[Notification]:
        """
            Return list of users with passed params.

            Result will be conjunctions(through params) of
            disjunctions(through id of id-params). So this method
            return obj, which must be in notification_ids, and connect with
            at least one user from user_ids if ids is not None.

            Args:
                notification_ids: list of notify which are permmited to return
                user_ids: list of user which must be connected
        """
        get_logger().info("Received request for getting notifications.")

        # for understanding this variable, see Tea._get_objects docstring
        join_infos = [
            (User, Notification.user, user_ids),
        ]

        query = self._get_objects(
            model=Notification,
            join_infos=join_infos,
        )

        if notification_ids is not None:
            query = query.filter(Notification.id.in_(notification_ids))

        result_objects = query.all()

        get_logger().debug(
            "Request of getting notifications is performed."
            " Returned {} notifications.".format(
                len(result_objects)
            )
        )
        return result_objects

    def get_model(self, type_ent: str) -> type:
        """
            Return model class by it's shortcup name. If
            shortcup name isn't exist, raise exception. Available
            shortcups mapper are keys of self.str_to_model_mapper.

            Raises:
                ValueError
        """
        get_logger().debug(
            "Received request for checking existing type '{}'.".format(
                type_ent
            )
        )
        error = EntityDontExistsError(
            "TeaTrancker unsupport entities with type {}".format(
                type_ent
            )
        )

        model = self.str_to_model_mapper.get(type_ent, None)

        if model is None:
            get_logger().error(
                "Tea doesn't contain type '{}'.".format(type_ent)
            )
            raise error

        return model

    def get_object(self, type_ent: str, id: int):
        model = self.get_model(type_ent)
        instance = self._get_object(model, id)

        return instance

    def _get_objects(self,
                     model: Any,
                     join_infos: List[Tuple[Any, Any, List[int]]] = None) -> Query:
        """
            Private method for implementation Tea.get_tasks, Tea.get_users, etc.
            Return sqlalchemy.orm.query.Query object, with objects of type 'model'.

            join_info - entity for implementation filtering on relationships
            join_info is a tuple (join_model, join_populates, join_ids):
                join_model - model from other side of relationship with 'model'
                join_populates - field of 'model' that is responsible for relathinship
                    with 'model'
                join_ids - list of ids of join_model

            Objects from the result query will be connected at least one join_model
            with id from join_ids through the join_populates for each join_info.

            Usage example:
                >>> join_infos = [
                    (Task, User.tasks, [1, 2, 3])
                    (SuperTask, User.supertasks, [4, 7])     
                ]
                >>> user_query = tea._get_objects(
                    model=User,
                    join_infos=join_infos,
                )
                >>> users = user_query.all()

            Args:
                model: type of entities which will be in return query
                join_infos: list of join_info - (Model, model.populates, ids),
                            see docstring for undersanding
        """

        query = self.session.query(model)

        for join_model, join_population, join_ids in join_infos:
            # it means that you do not need to make join
            if join_ids is None:
                continue

            query = query.join(join_population)
            query = query.filter(join_model.id.in_(join_ids))

        return query

    def _get_object(self, model: Any, id: int) -> Any:
        """
            Return object of type 'model' and id equal 'id'. If
            object don't exist raise exception.

            Args:
                model: type entity
                id: id of entity

            Raises:
                ValueError
        """
        get_logger().debug(
            "Received request for checking"
            " existing entity '{}' with id '{}'.".format(
                model.__name__,
                id,
            )
        )

        error = ObjectDontExistsError(
            "TeaTrancker doesn't contain {} with id {}".format(
                model.__name__,
                id
            )
        )

        query = self.session.query(model)
        query = query.filter(model.id == id)

        if query.count() == 0:
            raise error

        return query.first()
    # endregion

    def remove(self, type_ent: str, id: int):
        """
            Remove entity with type model of shortcup 'type_ent'
            with id equal 'id'. If not exist raise exception.
            All shortcup may see in keys of self.str_to_model_mapper

            Args:
                type_ent: string shortcup of type of entity
                id: id of entity

            Raises:
                ValueError
        """
        get_logger().info(
            "Received request for removing ent '{}' with id {}.".format(
                type_ent,
                id,
            )
        )

        model = self.get_model(type_ent)
        ent = self._get_object(model, id)

        self.session.delete(ent)
        self.session.commit()

    # region connecting
    # region privileges_connections
    def set_creator(self,
                    user_id: int,
                    task_id: int = None,
                    supertask_id: int = None):
        """
        Place user with id equal 'user_id' to the Task.creator_id and
        SuperTask.creator if task_id or supertask_id are not None.
        If user already in *.doers, raise exception.
        If task, supertask or user with this id doesn't exist, raise exception.
        If neither task_id nor supertask_id are passed, raise exception.

        Args:
            user_id: id of user, what will be placed
            task_id: id of task, what will be connected with user
            supertask_id: id of supertask, what will be connected with user

        Raises:
            ValueError
        """
        get_logger().debug("I was request for adding in doers")
        if task_id is None and supertask_id is None:
            raise ValueError(
                "You must pass at least 'task_id' or 'supertask_id'."
            )

        get_logger().debug("I was request for setting creator")

        user = self._get_object(User, user_id)
        if task_id is not None:
            task = self._get_object(Task, task_id)
            task.creator = user

        if supertask_id is not None:
            supertask = self._get_object(SuperTask, supertask_id)
            supertask.creator = user

        self.session.commit()

    def add_moderator(self,
                      user_id: int,
                      task_id: int = None,
                      supertask_id: int = None):
        """
        Place user with id equal 'user_id' to the populates Task.moderators and
        SuperTask.moderators if task_id or supertask_id are not None.
        If user already in *.moderators, raise exception.
        If task, supertask or user with this id doesn't exist, raise exception.
        If neither task_id nor supertask_id are passed, raise exception.

        Args:
            user_id: id of user, what will be placed
            task_id: id of task, what will be connected with user
            supertask_id: id of supertask, what will be connected with user

        Raises:
            ValueError
        """
        get_logger().debug("I was request for adding in moderators")
        if task_id is None and supertask_id is None:
            raise ValueError(
                "You must pass at least 'task_id' or 'supertask_id'."
            )

        error_msg = "User {} is alredy in 'moderators' of {} {}"
        user = self._get_object(User, user_id)

        if task_id is not None:
            task = self._get_object(Task, task_id)
            if user in task.moderators:
                raise ValueError(
                    error_msg.format(user_id, "Task", task_id)
                )

            task.moderators.append(user)

        if supertask_id is not None:
            supertask = self._get_object(SuperTask, supertask_id)
            if user in supertask.moderators:
                raise ValueError(
                    error_msg.format(user_id, "SuperTask", supertask_id)
                )

            supertask.moderators.append(user)

        self.session.commit()

    def remove_moderator(self,
                         user_id: int,
                         task_id: int = None,
                         supertask_id: int = None):
        """
        Remove user with id equal 'user_id' from the populates Task.moderators and
        SuperTask.moderators if task_id or supertask_id are not None.
        If user is not in *.moderators yet, raise exception.
        If task, supertask or user with this id doesn't exist, raise exception.
        If neither task_id nor supertask_id are passed, raise exception.

        Args:
            user_id: id of user, what will be removed
            task_id: id of task, what will be disconnected with user
            supertask_id: id of supertask, what will be disconnected with user

        Raises:
            ValueError
        """
        get_logger().debug("I was request for removing from moderators")
        if task_id is None and supertask_id is None:
            raise ValueError(
                "You must pass at least 'task_id' or 'supertask_id'."
            )

        error_msg = "User {} is not in 'moderators' of {} {} yet"
        user = self._get_object(User, user_id)

        if task_id is not None:
            task = self._get_object(Task, task_id)
            if user not in task.moderators:
                raise ValueError(
                    error_msg.format(user_id, "Task", task_id)
                )

            task.moderators.remove(user)

        if supertask_id is not None:
            supertask = self._get_object(SuperTask, supertask_id)
            if user not in supertask.moderators:
                raise ValueError(
                    error_msg.format(user_id, "SuperTask", supertask_id)
                )

            supertask.moderators.remove(user)

        self.session.commit()

    def add_doer(self,
                 user_id: int,
                 task_id: int = None,
                 supertask_id: int = None):
        """
        Place user with id equal 'user_id' to the populates Task.doers and
        SuperTask.doers if task_id or supertask_id are not None.
        If user already in *.doers, raise exception.
        If task, supertask or user with this id doesn't exist, raise exception.
        If neither task_id nor supertask_id are passed, raise exception.

        Args:
            user_id: id of user, what will be placed
            task_id: id of task, what will be connected with user
            supertask_id: id of supertask, what will be connected with user

        Raises:
            ValueError
        """
        get_logger().debug("I was request for adding in doers")
        if task_id is None and supertask_id is None:
            raise ValueError(
                "You must pass at least 'task_id' or 'supertask_id'."
            )

        error_msg = "User {} is alredy in 'doers' of {} {}"
        user = self._get_object(User, user_id)

        if task_id is not None:
            task = self._get_object(Task, task_id)
            if user in task.doers:
                raise ValueError(
                    error_msg.format(user_id, "Task", task_id)
                )

            task.doers.append(user)

        if supertask_id is not None:
            supertask = self._get_object(SuperTask, supertask_id)
            if user in supertask.doers:
                raise ValueError(
                    error_msg.format(user_id, "SuperTask", supertask_id)
                )

            supertask.doers.append(user)

        self.session.commit()

    def remove_doer(self,
                    user_id: int,
                    task_id: int = None,
                    supertask_id: int = None):
        """
        Remove user with id equal 'user_id' from the populates Task.doers and
        SuperTask.doers if task_id or supertask_id are not None.
        If user is not in *.doers yet, raise exception.
        If task, supertask or user with this id doesn't exist, raise exception.
        If neither task_id nor supertask_id are passed, raise exception.

        Args:
            user_id: id of user, what will be removed
            task_id: id of task, what will be disconnected with user
            supertask_id: id of supertask, what will be disconnected with user

        Raises:
            ValueError
        """
        get_logger().debug("I was request for removing from doers")
        if task_id is None and supertask_id is None:
            raise ValueError(
                "You must pass at least 'task_id' or 'supertask_id'."
            )

        error_msg = "User {} is not in 'doers' of {} {} yet"
        user = self._get_object(User, user_id)

        if task_id is not None:
            task = self._get_object(Task, task_id)
            if user not in task.doers:
                raise ValueError(
                    error_msg.format(user_id, "Task", task_id)
                )

            task.doers.remove(user)

        if supertask_id is not None:
            supertask = self._get_object(SuperTask, supertask_id)
            if user not in supertask.doers:
                raise ValueError(
                    error_msg.format(user_id, "SuperTask", supertask_id)
                )

            supertask.doers.remove(user)

        self.session.commit()

    def add_watcher(self,
                    user_id: int,
                    task_id: int = None,
                    supertask_id: int = None):
        """
        Place user with id equal 'user_id' to the populates Task.watchers and
        SuperTask.watchers if task_id or supertask_id are not None.
        If user already in *.watchers, raise exception.
        If task, supertask or user with this id doesn't exist, raise exception.
        If neither task_id nor supertask_id are passed, raise exception.

        Args:
            user_id: id of user, what will be placed
            task_id: id of task, what will be connected with user
            supertask_id: id of supertask, what will be connected with user

        Raises:
            ValueError
        """
        get_logger().debug("I was request for adding in watchers")
        if task_id is None and supertask_id is None:
            raise ValueError(
                "You must pass at least 'task_id' or 'supertask_id'."
            )

        error_msg = "User {} is alredy in 'watchers' of {} {}"
        user = self._get_object(User, user_id)

        if task_id is not None:
            task = self._get_object(Task, task_id)
            if user in task.watchers:
                raise ValueError(
                    error_msg.format(user_id, "Task", task_id)
                )

            task.watchers.append(user)

        if supertask_id is not None:
            supertask = self._get_object(SuperTask, supertask_id)
            if user in supertask.watchers:
                raise ValueError(
                    error_msg.format(user_id, "SuperTask", supertask_id)
                )

            supertask.watchers.append(user)

        self.session.commit()

    def remove_watcher(self,
                       user_id: int,
                       task_id: int = None,
                       supertask_id: int = None):
        """
        Remove user with id equal 'user_id' from the populates Task.watchers and
        SuperTask.watchers if task_id or supertask_id are not None.
        If user is not in *.watchers yet, raise exception.
        If task, supertask or user with this id doesn't exist, raise exception.
        If neither task_id nor supertask_id are passed, raise exception.

        Args:
            user_id: id of user, what will be removed
            task_id: id of task, what will be disconnected with user
            supertask_id: id of supertask, what will be disconnected with user

        Raises:
            ValueError
        """
        get_logger().debug("I was request for removing from watchers")
        if task_id is None and supertask_id is None:
            raise ValueError(
                "You must pass at least 'task_id' or 'supertask_id'."
            )

        error_msg = "User {} is not in 'watchers' of {} {} yet"
        user = self._get_object(User, user_id)

        if task_id is not None:
            task = self._get_object(Task, task_id)
            if user not in task.watchers:
                raise ValueError(
                    error_msg.format(user_id, "Task", task_id)
                )

            task.watchers.remove(user)

        if supertask_id is not None:
            supertask = self._get_object(SuperTask, supertask_id)
            if user not in supertask.watchers:
                raise ValueError(
                    error_msg.format(user_id, "SuperTask", supertask_id)
                )

            supertask.watchers.remove(user)

        self.session.commit()
    # endregion

    def mark_with_tag(self,
                      tag_id: int,
                      task_id: int = None,
                      supertask_id: int = None):
        """
        Place tag with id equal 'tag_id' to the populates Task.tags and
        SuperTask.tags if task_id or supertask_id are not None.
        If tag already in *.tags raise exception.
        If task, supertask or tag with this id doesn't exist, raise exception.
        If neither task_id nor supertask_id are passed, raise exception.

        Args:
            tag_id: id of tag, what will be placed
            task_id: id of task, what will be connected with tag
            supertask_id: id of supertask, what will be connected with tag

        Raises:
            ValueError
        """
        get_logger().debug("I was request for marking with tag")
        if task_id is None and supertask_id is None:
            raise ValueError(
                "You must pass at least 'task_id' or 'supertask_id'."
            )

        error_msg = "Tag {} is alredy in 'tags' of {} {}"
        tag = self._get_object(Tag, tag_id)

        if task_id is not None:
            task = self._get_object(Task, task_id)
            if tag in task.tags:
                raise ValueError(
                    error_msg.format(tag_id, "Task", task_id)
                )

            task.tags.append(tag)

        if supertask_id is not None:
            supertask = self._get_object(SuperTask, supertask_id)
            if tag in supertask.tags:
                raise ValueError(
                    error_msg.format(tag_id, "SuperTask", supertask_id)
                )

            supertask.tags.append(tag)

        self.session.commit()

    def unmark_with_tag(self,
                        tag_id: int,
                        task_id: int = None,
                        supertask_id: int = None):
        """
        Remove tag with id equal 'tag_id' from the populates Task.tags and
        SuperTask.tags if task_id or supertask_id are not None.
        If tag is not in *.doers yet, raise exception.
        If task, supertask or tag with this id doesn't exist, raise exception.
        If neither task_id nor supertask_id are passed, raise exception.

        Args:
            tag_id: id of tag, what will be removed
            task_id: id of task, what will be disconnected with tag
            supertask_id: id of supertask, what will be disconnected with tag

        Raises:
            ValueError
        """
        get_logger().debug("I was request for unmarkin with tag")
        if task_id is None and supertask_id is None:
            raise ValueError(
                "You must pass at least 'task_id' or 'supertask_id'."
            )

        error_msg = "Tag {} is not in 'doers' of {} {} yet"
        tag = self._get_object(Tag, tag_id)

        if task_id is not None:
            task = self._get_object(Task, task_id)
            if tag not in task.tags:
                raise ValueError(
                    error_msg.format(tag_id, "Task", task_id)
                )

            task.tags.remove(tag)

        if supertask_id is not None:
            supertask = self._get_object(SuperTask, supertask_id)
            if tag not in supertask.tags:
                raise ValueError(
                    error_msg.format(tag_id, "SuperTask", supertask_id)
                )

            supertask.tags.remove(tag)

        self.session.commit()

    def _check_cicle_dependence(self, source: Task, target: Task):
        """
            If we can walk from source to target through args(task.subtasks),
            raise exception. Uses bfs.

            Raises:
                ValueError
        """
        nonrelaxed = Queue()
        visited = set()

        visited.add(source.id)
        nonrelaxed.put(source)
        while not nonrelaxed.empty():
            current_vertex = nonrelaxed.get()

            if current_vertex.id == target.id:
                raise CicleDependenceError(
                    subtask_id=source.id,
                    overtask_id=target.id,
                )

            for next_vertex in current_vertex.subtasks:
                if next_vertex.id not in visited:
                    visited.add(next_vertex.id)
                    nonrelaxed.put(next_vertex)

        self.session.commit()

    def add_dependence(self, parent_id: int, child_id: int):
        """
            Add dependence from parent taks to child task. If
            at least one not exist, raise exception. If dependence is
            exist, raise exception.

            Args:
                parent_id: id of parent task
                child_id: id of child task

            Raises:
                ValueError
        """
        get_logger().debug("I was request for adding dependence.")

        parent_task = self._get_object(Task, parent_id)
        child_task = self._get_object(Task, child_id)
        # anticipate cicle dependence
        self._check_cicle_dependence(source=child_task, target=parent_task)

        if child_task in parent_task.subtasks:
            raise ValueError(
                "Task {} already is"
                " parent of task {}".format(
                    parent_id,
                    child_id,
                )
            )

        # anticipate case: parent is done, but child isn't done
        if not child_task.is_done and parent_task.is_done:
            raise ValueError(
                "Parent task {} is already done, but child task {}"
                " is not done yet. Adding dependence lead to"
                " incorrect structure.".format(parent_id, child_id)
            )

        parent_task.subtasks.append(child_task)
        self.session.commit()

    def remove_dependence(self, parent_id: int, child_id: int):
        """
            Remove dependence from parent taks to child task. If
            at least one not exist, raise exception. If dependence is
            not exist, raise exception.

            Args:
                parent_id: id of parent task
                child_id: id of child task

            Raises:
                ValueError
        """
        get_logger().debug("I was request for removing dependence.")

        parent_task = self._get_object(Task, parent_id)
        child_task = self._get_object(Task, child_id)
        if child_task not in parent_task.subtasks:
            raise ValueError(
                "Task {} isn't parent"
                " of Task {} yet.".format(
                    parent_id,
                    child_id,
                )
            )

        parent_task.subtasks.remove(child_task)
        self.session.commit()

    def add_trust(self, dominant_id: int, submissive_id: int):
        """
            Add trust from User submissive_id to User dominant_id. If
            at least one not exist, raise exception. If trust is
            exist, raise exception.

            Args:
                dominant_id: id of dominant user
                submissive_id: id of submissive user

            Raises:
                ValueError
        """
        get_logger().debug("I was request for adding trust.")

        dominant_user = self._get_object(User, dominant_id)
        submissive_user = self._get_object(User, submissive_id)

        if submissive_user in dominant_user.trustings:
            raise ValueError(
                "User with id {} already trust"
                " user with id {}".format(
                    submissive_user.id,
                    dominant_user.id,
                )
            )

        dominant_user.trustings.append(submissive_user)
        self.session.commit()

    def remove_trust(self, dominant_id: int, submissive_id: int):
        """
            Remove trust from User submissive_id to User dominant_id. If
            at least one not exist, raise exception. If trust is
            exist, raise exception.

            Args:
                dominant_id: id of dominant user
                submissive_id: id of submissive user

            Raises:
                ValueError
        """
        get_logger().debug("I was request for removing trust.")

        dominant_user = self._get_object(User, dominant_id)
        submissive_user = self._get_object(User, submissive_id)

        if submissive_user not in dominant_user.trustings:
            raise ValueError(
                "User with id {} hasn't trust"
                " user with id {} yet".format(
                    submissive_user.id,
                    dominant_user.id,
                )
            )

        dominant_user.trustings.remove(submissive_user)
        self.session.commit()

    def _check_completed_subtasks(self, id: int):
        """
        Raise exception if there is subtask of task that is not done.
        
        Args:
            id: id of task

        Raises:
            ValueError
        """
        get_logger().debug(
            "Received request for checking completing subtask "
            " of task with id {}".format(id)
        )

        task = self._get_object(Task, id=id)

        for subtask in task.subtasks:
            if not subtask.is_done:
                get_logger().error(
                    "Subtask {} is not completed.".format(
                        subtask.id
                    )
                )

                raise ValueError(
                    "Task {} has uncompleted subtask"
                    " {}".format(task.id, subtask.id)
                )

    def check_uncompleted_overtasks(self, id: int):
        """
        Raise exception if there is overtask of task that is done.
         
        Args:
            id: id of task

        Raises:
            ValueError
        """
        get_logger().debug(
            "Received request for checking uncompleting overtask "
            " of task with id {}".format(id)
        )

        task = self._get_object(Task, id=id)

        for overtask in task.overtasks:
            if overtask.is_done:
                get_logger().error(
                    "Overtask {} is completed.".format(
                        overtask.id
                    )
                )

                raise ValueError(
                    "Task {} already has completed overtask"
                    " {}".format(task.id, overtask.id)
                )
    # endregion

    # region completing
    def complete_task(self,
                      id: int,
                      force: bool = False,
                      execution_time: Datetime = None):
        """
            If all subtasks of taks are done, mark task as done, else
            raise exception. If passed force, complete all subtasks with force.

            Args:
                id: id of task
                execution_time: default datetime.now(), but may be passed explicit
            
            Raises:
                ValueError
        """
        get_logger().info(
            "Received request for completing task {}".format(id)
        )

        if execution_time is None:
            execution_time = datetime.now()

        task = self._get_object(Task, id)

        if force:
            for subtask in task.subtasks:
                if not subtask.is_done:
                    self.complete_task(subtask.id, force=True)
        else:
            self._check_completed_subtasks(id)

            if task.is_done:
                raise ValueError(
                    "Task with id {} is already done.".format(id)
                )

        get_logger().info(
            "Task {} is successfuly completed".format(id)
        )
        task.is_done = True
        task.execution_time = execution_time

        self.session.commit()

    def resume_task(self, id: int, force: bool = False):
        """
            If all overtasks of taks are not done, mark task as not done, else
            raise exception. If passed force, resume all overtasks with force.

            Args:
                id: id of task

            Raises:
                ValueError
        """
        get_logger().info(
            "Received request for uncompleting task {}".format(id)
        )

        task = self._get_object(Task, id)

        if force:
            for overtask in task.overtasks:
                if overtask.is_done:
                    self.resume_task(overtask.id, force=True)
        else:
            self.check_uncompleted_overtasks(id)

            if not task.is_done:
                raise ValueError(
                    "Task with id {} is not done yet.".format(id)
                )

        get_logger().info(
            "Task {} is successfuly uncompleted".format(id)
        )
        task.is_done = False
        task.execution_time = None

        self.session.commit()
    # endregion

    # region synchronization
    def _generate_task(self, supertask: SuperTask):
        """Generate task by supertask."""
        task_id = self.add_task(
            title=supertask.title,
            description=supertask.description,
            creation_time=supertask.next_creation_time,
            deadline=(supertask.next_creation_time +
                      supertask.time_to_execution),
        )

        self.set_creator(
            user_id=supertask.creator_id,
            task_id=task_id,
        )

        for user in supertask.moderators:
            self.add_moderator(
                user_id=user.id,
                task_id=task_id,
            )

        for user in supertask.doers:
            self.add_doer(
                user_id=user.id,
                task_id=task_id,
            )

        for user in supertask.watchers:
            self.add_watcher(
                user_id=user.id,
                task_id=task_id,
            )

        for tag in supertask.tags:
            self.mark_with_tag(
                tag_id=tag.id,
                task_id=task_id,
            )

    def _generate_notification(self,
                               kind: NotificationKind,
                               user_id: int = None,
                               task_id: int = None):
        """
        Add notification and connect it with user_id with passed kind.

        Args:
            kind: kind of notification
            user_id: id of user, what will be connected with notification
            task_id: need only for description of OVERDUE notification
        """
        if kind == NotificationKind.OVERDUE_TASK:
            description = ("Task {}, which connected with"
            " you, has expired.").format(task_id)
        elif kind == NotificationKind.NEW_COMMENT:
            description = ("Task {}, which connected with"
            " you, has been commented.").format(task_id)
        else:
            description = "Someting happend."

        notification_id = self.add_notification(
            kind,
            description=description,
            user_id=user_id,
        )

    def synchronize_time(self,
                         current_time: Datetime,
                         generate_notifications: bool = False):
        """
            Synchronize task's expiration status with 'current_time' and
            generate task by supertask if it's time. Also generage
            notification if 'generate_notifications' is True.
        """
        get_logger().info(
            "Received request for synchronization time for"
            " current_time: {}. Generation_notification: {}".format(
                current_time,
                generate_notifications,
            )
        )

        # Check generating tasks by supertasks
        for supertask in self.get_supertasks():
            # Interval kind
            if supertask.kind == SuperTaskKind.INTERVAL_KIND:
                re_creation_period = supertask.re_creation_period

                while supertask.next_creation_time < current_time:
                    self._generate_task(supertask)
                    supertask.next_creation_time += re_creation_period

                self.session.commit()
            # Week kind
            elif supertask.kind == SuperTaskKind.WEEK_KIND:
                one_day_delta = timedelta(days=1)

                self._update_next_creation_supertask(supertask.id)

                while supertask.next_creation_time < current_time:
                    self._generate_task(supertask)
                    supertask.next_creation_time += one_day_delta
                    self._update_next_creation_supertask(supertask.id)
            else:
                raise NotImplementedError(
                    "'{}' type of supertask not implemented yet".format(
                        supertask.kind
                    )
                )

        # Mark expiration of tasks
        for task in self.get_tasks():
            if task.deadline < current_time:

                # generating notiication
                if generate_notifications and not task.is_expired:
                    for user in task.doers:
                        self._generate_notification(
                            kind=NotificationKind.OVERDUE_TASK,
                            user_id=user.id,
                            task_id=task.id,
                        )

                task.is_expired = True
            else:
                task.is_expired = False

        self.session.commit()
    # endregion

    def _update_next_creation_supertask(self, supertask_id: int):
        """
        Set next_creation_time on first valid moment after
        supertask.next_creation_time for supertask.
        Have a meaning only for Week kind of SuperTask.
        """
        supertask = self._get_object(SuperTask, supertask_id)

        if supertask.kind != SuperTaskKind.WEEK_KIND:
            return

        old_next_creation_time = supertask.next_creation_time
        weekday = old_next_creation_time.weekday()
        for shift in range(7):
            value = (weekday + shift) % 7
            # print(supertask.week_mask[value])
            if supertask.week_mask[value] == "1":
                delta = timedelta(days=shift)

                new_next_creation_time = old_next_creation_time + delta
                supertask.next_creation_time = new_next_creation_time
                break

        self.session.commit()

    def get_task_tree(self, task_id: int) -> dict:
        """
        Return hierarchically nested structure of task tree. It
        cannot be infinity, because cicle dependece are anticipated.
        It implement through recursion.

        Base component(call it TaskStruct) is:
        {
            "id": <task_id: int>,
            "subtasks": <list of TaskStruct>,
        }

        Args:
            task_id: id of task
        """
        result = {}

        task = self._get_object(Task, task_id)
        result["id"] = task_id

        result["subtasks"] = [
            self.get_task_tree(subtask.id) for subtask in task.subtasks
        ]

        return result
