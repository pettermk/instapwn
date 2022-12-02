import functools
import pickle
from typing import Any, Callable, Dict, Optional


from django.core.cache.backends.base import BaseCache, DEFAULT_TIMEOUT

from dapr.clients import DaprClient

DAPR_STORE_NAME = 'django_cache'

def omit_exception(
    method: Optional[Callable] = None, return_value: Optional[Any] = None
):
    """
    Simple decorator that intercepts connection
    errors and ignores these if settings specify this.
    """

    if method is None:
        return functools.partial(omit_exception, return_value=return_value)

    @functools.wraps(method)
    def _decorator(self, *args, **kwargs):
        try:
            return method(self, *args, **kwargs)
        except Exception as e:
            if self._ignore_exceptions:
                if self._log_ignored_exceptions:
                    self.logger.exception("Exception ignored")

                return return_value
            raise e.__cause__

    return _decorator

class DaprCache(BaseCache):
    pickle_protocol = pickle.HIGHEST_PROTOCOL
    def __init__(self, server: str, params: Dict[str, Any]) -> None:
        super().__init__(params)
        self._client = None

    @property
    def client(self):
        """
        Lazy client connection property.
        """
        if self._client is None:
            self._client = DaprClient(address='localhost:50002')
        return self._client

    @omit_exception
    def set(self, *args, **kwargs):
        return self.client.set(*args, **kwargs)

    @omit_exception
    def incr_version(self, *args, **kwargs):
        return self.client.incr_version(*args, **kwargs)

    @omit_exception
    def add(self, key, value, timeout=DEFAULT_TIMEOUT, version=None):
        key = self.make_and_validate_key(key, version=version)
        pickled = pickle.dumps(value, self.pickle_protocol)
        return self.client.save_state(
            DAPR_STORE_NAME,
            key,
            pickled,
            state_metadata={
                'ttlInSeconds': str(timeout)
            }
        )

    def get(self, key, default=None, version=None, client=None):
        key = self.make_and_validate_key(key, version=version)
        state = self.client.get_state(DAPR_STORE_NAME, key)
        if state.data:
            return pickle.loads(state.data)
        return None

    def set(self, key, value, timeout=DEFAULT_TIMEOUT, version=None):
        key = self.make_and_validate_key(key, version=version)
        pickled = pickle.dumps(value, self.pickle_protocol)
        self.client.save_state(
            DAPR_STORE_NAME,
            key,
            pickled,
            state_metadata={
                'ttlInSeconds': str(timeout)
            }
        )

    def touch(self, key, timeout=DEFAULT_TIMEOUT, version=None):
        key = self.make_and_validate_key(key, version=version)
        state = self.client.get_state(DAPR_STORE_NAME, key)
        if not state:
            return False
        self.client.save_state(
            DAPR_STORE_NAME,
            key,
            state.data,
            state_metadata={
                'ttlInSeconds': str(timeout)
            }
        )
        return True

    def incr(self, key, delta=1, version=None):
        key = self.make_and_validate_key(key, version=version)
        state = self.client.get_state(DAPR_STORE_NAME, key)
        if not state:
            raise ValueError("Key '%s' not found" % key)
        value = pickle.loads(state.data)
        new_value = value + delta
        pickled = pickle.dumps(new_value, self.pickle_protocol)
        self.client.save_state(
            DAPR_STORE_NAME,
            key,
            pickled
        )
        return new_value

    def has_key(self, key, version=None):
        key = self.make_and_validate_key(key, version=version)
        state = self.client.get_state(DAPR_STORE_NAME, key)
        if not state:
            return False
        return True

    def delete(self, key, version=None):
        key = self.make_and_validate_key(key, version=version)
        self.client.delete_state(DAPR_STORE_NAME, key)

    # TODO
    def clear(self):
        pass
