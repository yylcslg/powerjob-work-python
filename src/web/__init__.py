from flask import Blueprint

worker = Blueprint('worker',__name__, url_prefix='/worker')
taskTracker = Blueprint('taskTracker',__name__, url_prefix='/taskTracker')
processorTracker = Blueprint('processorTracker',__name__, url_prefix='/processorTracker')

from . import workerActor