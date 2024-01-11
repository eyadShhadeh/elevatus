from typing import Any, Dict, Generic, List, Optional, Tuple, TypeVar
from pydantic.generics import GenericModel
DataT = TypeVar('DataT')


class APIResponse(GenericModel, Generic[DataT]):
    """
        A generic response model
    """
    success: bool = True
    metadata: Optional[Dict[str, str]] = None
    errors: Optional[Tuple[str, ...]] = None
    debug: Optional[Tuple[str, ...]] = None
    results: Optional[DataT] = None
