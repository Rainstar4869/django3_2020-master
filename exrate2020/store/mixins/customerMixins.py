from django.core.exceptions import FieldDoesNotExist
from django.db.models import ManyToManyField, ManyToOneRel


class DoesNotExist(object):
    pass


class ModelUpdateFieldsMixin(object):
    """
    Model对象在save的时候如果没有传update_fields参数，则自动跟踪对象字段的修改，并且在save的时候自动加上update_fields
    """

    def __init__(self, *args, **kwargs):
        super(ModelUpdateFieldsMixin, self).__init__(*args, **kwargs)

        self._changed_fields = {}  # 初始化字典，用户存储字段变更的信息

    def __setattr__(self, name, value):
        """
        重写__setattr__方法用于对属性赋值检测
        """

        if hasattr(self, '_changed_fields'):
            try:
                field = self._meta.get_field(name)  # 通过属性名称获取field对象，如果不是field属性则忽略
            except FieldDoesNotExist:
                field = None
            if field and not (field.auto_created or field.hidden) and field.__class__ not in (
                    ManyToManyField, ManyToOneRel):  # 如果不是自动创建，隐藏字段，多对多，多对一的关联对象
                try:
                    old = getattr(self, name, DoesNotExist)  # 获取赋值前的属性值
                except field.rel.to.DoesNotExist:
                    old = DoesNotExist

                super(ModelUpdateFieldsMixin, self).__setattr__(name, value)  # 赋值
                new = getattr(self, name, DoesNotExist)  # 获取新的属性值
                try:
                    changed = (old != new)  # 比较
                except:
                    changed = True
                if changed:  # 如果发现值变更了
                    changed_fields = self._changed_fields
                    if name in changed_fields:  # 如果已经记录过且值与新的值一样，则忽略
                        if changed_fields[name] == new:
                            changed_fields.pop(name)
                    else:
                        # changed_fields[name] = copy(old)  # 记录老的值
                        changed_fields[name] = old  # 记录老的值
            else:
                super(ModelUpdateFieldsMixin, self).__setattr__(name, value)
        else:
            super(ModelUpdateFieldsMixin, self).__setattr__(name, value)

    def save(self, *args, **kwargs):
        """
        重写save方法，传update_fields参数
        """
        if not self._state.adding and hasattr(self,
                                              '_changed_fields') and 'update_fields' not in kwargs and not kwargs.get(
                'force_insert', False):
            kwargs['update_fields'] = [key for key, value in self._changed_fields.iteritems() if hasattr(self, key)]
            self._changed_fields = {}
        return super(ModelUpdateFieldsMixin, self).save(*args, **kwargs)
