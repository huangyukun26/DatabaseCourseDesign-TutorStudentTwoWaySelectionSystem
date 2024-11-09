from typing import TypeVar, Generic, List, Optional, Type
from django.db.models import Model

T = TypeVar('T', bound=Model)

class BaseDAO(Generic[T]):
    """基础DAO接口"""
    
    def __init__(self, model_class: Type[T]):
        self.model_class = model_class
    
    def insert(self, **kwargs) -> T:
        """插入一条记录"""
        return self.model_class.objects.create(**kwargs)
    
    def find_by_id(self, id: int) -> Optional[T]:
        """根据ID查找记录"""
        try:
            return self.model_class.objects.get(pk=id)
        except self.model_class.DoesNotExist:
            return None
    
    def find_all(self) -> List[T]:
        """查找所有记录"""
        return list(self.model_class.objects.all())
    
    def update(self, instance: T, **kwargs) -> T:
        """更新记录"""
        for key, value in kwargs.items():
            setattr(instance, key, value)
        instance.save()
        return instance
    
    def delete(self, instance: T) -> bool:
        """删除记录"""
        instance.delete()
        return True 