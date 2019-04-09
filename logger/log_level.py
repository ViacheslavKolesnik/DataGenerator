from enum import Enum


# log levels enumeration
class LogLevel(Enum):
	TRACE = 0
	DEBUG = 1
	INFO = 2
	WARN = 3
	ERROR = 4
	CRITICAL = 5
	FATAL = 6
