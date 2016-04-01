from django.db import models
from django.contrib.auth.models import User
import enum
from django.core.exceptions import ValidationError

import sys

_CHARFIELD_NAME_MAX_LENGTH = 16
_CHARFIELD_TEXT_MAX_LENGTH = 128

"""
Do Steps, project management system
===================================

Preamble
--------
The word 'project' is defined in the dictionary as: "an individual or 
collaborative enterprise that is carefully planned to achieve a particular aim."
The latin root of project is proiectum, meaning 'something thrown forth'.

The process of a project is that a past situation is analysed judged as less 
favourable compared to a future hypothetical situation. Thus identifying the
current environment and defining what a future environment could be. When
comparing the two environments, the difference is a set of outlines.

Criteria
--------
Whether the project can be executed is dependent if the outlines can pass the
following criteria:
- Is it theoretically possible?
- Is it practically possible? (e.g. do we have sufficient resources)
- Will the expected gain outweigh the expenditure required for the change?
- Can the change be done before it becomes irrelevant?

An Example
---------- 
The current situation is that I am reading a text and I think I will enjoy it
more if I have a coffee with it, other beverages are available, but for 
simplicity sake I stick with hot instant coffee, without sugar or milk.

Thus my current situation is, I don't have a coffee.
My future hypothetical situation is, I have a coffee.
So my outline is: make a coffee.

Theoretically coffee making is possible, even if I have never made a coffee or 
seen anyone make a coffee, there are similar processes (like making a tea) that 
shows no principal objections.
 
To make a coffee, I need a means of heating water, access to coffee, a cup, 
and some time to do it. As I have all these, it is also possible in a practical
sense.

Is the cost of the coffee (I'll say around 20p and 5 minutes time) worth the
gain in productivity and satisfaction? Yes I would think so.

I should not drink coffee after 5 in the afternoon as it will take me too long 
to fall asleep at night. It is now 3 o'clock so yes I can make and drink my
coffee before that time.

Bigger Projects
---------------
The criteria remain the same, regardless if it is a small familiar task or a big
project never tried before. However in the latter case, I may not be able to 
answer the criteria as there are too many unknowns. To reduce the unknowns, I
need to brake down the outlines into smaller portions. Large enough so I don't 
waste time that could have been used on executing it, but detailed enough so I 
can judge whether they can pass the criteria. The actual level of detail depends
on experience, the more experienced someone is, the less details are required 
for that person to be confident in a correct judgement. This is due to see
parallels with past project that are approximately.

Fleshing out the details
------------------------
Now that I have broken down the project and confirmed that it is a valid effort,
the details need to be fleshed out. My first step would be to ask a business
analyst to provide me a list of items that I need to be resolved with the
proposed solution, this will often be just comments on the existing structure.
Next I will need an subject matter expert to see if there is an existing 
framework to follow. If there is a framework, I need to restructure my project 
to conform with this framework. If there is not a framework, I need an architect
to create a framework according to the best practises. If there is not a best
practice I need the business analyst to draw one up before that.

Assuming that the project structure is rearranged according to the requirements,
I need to label the tasks that are required to create a minimum valid product 
(MVP) that still fits within the framework.

All the other tasks are ignored for now and put on the backlog.
Now I assign the tasks to senior members of the team that will then further
split these tasks out in items that can be done within a days worth of work.

During all of the above I will need to keep checking if the criteria can still
be met.

The Software
------------
Starting and splitting out the project is done intuitively, by just adding a 
task, if the task is to big it is split out into sub-task. The parent task will
no longer contain actionable tasks and as such only serves as a container to the
children.

All items (whether tasks or containers) can have multiple dependencies, which
can be simply selected from the overview.

Each task can be assigned an estimated time, actual time spend and progress.
As all digital work needs to be saved in a revision controlled storage system,
commit messages are cross referenced with the task. If a task is physical, the
logbook containing the signed off work (which should be digital) is used as a
digital cross reference.


Workflow Management
-------------------
The tasks related to a project all have in common that they are planned 
activities. But this is only a small part of tasks, there are also recurring
tasks (for example sending out a birthday card) and incidental tasks (something 
got broken or someone needs help with it). Maintenance is the remaining
category of tasks. Maintenance is required, if the fall out of a problem due to
non-maintenance results in catastrophic failure or severe costs to the business
so that is warrants the continuous cost of maintenance. 

What all tasks have in common is that they end-up as an actionable item that
is in the priority todo list of the one who actually does the work.

So all items need to have an association with who created the item, how much
time is budgeted, how much time is spend on it, and who spend that time. They 
also need a deadline when the task must be finished (this should not be a soft 
deadline, but a hard one with real consequences.

Interfaces
----------
For Project Initiators;
There is the concept map like interface, with lines that can be drawn between 
items to indicate dependencies.

For Project Managers;
The outlines in the concept map are goals in the calendar/task matrix.
Various status displays like run chart, burn-down, gantt, etc.

For Team Leads;
A Kanban board with prioritised to do, in progress and done.

For Team Members;
A list of prioritised tasks.


"""
    
class Name(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = _CHARFIELD_NAME_MAX_LENGTH
        kwargs['unique'] = True
        models.CharField.__init__(self, *args, **kwargs)
        
class Description(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = _CHARFIELD_TEXT_MAX_LENGTH
        kwargs['null'] = True
        kwargs['blank'] = True
        models.CharField.__init__(self, *args, **kwargs)
        

class _Abstract(models.Model):
    class Meta:
        """
        """
        abstract = True

    dts_insert = models.DateTimeField(auto_now_add=True)
    dts_update = models.DateTimeField(auto_now=True)
    dts_delete = models.DateTimeField(null=True, blank=True, editable=False)
    
    def __str__(self):
        txt = ("{__name__}({id}) # {content}")
        tmp = self.__dict__.copy()
        tmp['__name__'] = self.__class__.__name__
        tmp['content'] = list()
        
        keys = list(self.__dict__.keys())
        keys.sort()
        for key in keys:
            if not key.startswith('_'):
                if key != 'id':
                    value = key+':'+str(tmp[key])+ ' | '
                    tmp['content'].append(value)
            
        tmp['content'] = "".join(tmp['content'])

        returns = txt.format(**tmp).strip() 
        return returns
    
    
class _NameDescription(_Abstract):
    class Meta(_Abstract.Meta):
        abstract = True
    name = Name()
    description = Description()
    
    def __str__(self):
        text = "{id}:{name}"
        return text.format(**self.__dict__)

class _SelfReferenceNameDescription(_NameDescription):
    class Meta(_NameDescription.Meta):
        abstract = True
    parent = models.ForeignKey("self")
    
    def __str__(self):
        text = self.name
        if self.parent.id != self.id:
            text = str(self.parent) + '>' + text
        return text
    

class Workflow(_SelfReferenceNameDescription):
    class Meta(_Abstract.Meta):
        unique_together = ('parent', 'name')

    # UNASSESSED  #
    # SUPPORT     #
    # SCHEDULED   #
    # MAINTENANCE #
    # DEVELOPMENT #
    pass

class Attribute(_NameDescription): pass
    
        
class AttributeWorkflow(_Abstract):
    class Meta(_Abstract.Meta):
        unique_together = ('attribute', 'workflow')

    attribute = models.ForeignKey(Attribute)
    workflow = models.ForeignKey(Workflow)
    
class NamedAttributeWorkflow(_NameDescription):
    attribute_workflow_entries = models.ManyToManyField(AttributeWorkflow)
    

class Item(_SelfReferenceNameDescription):
    workflow = models.ForeignKey(Workflow)
    identifier = models.ForeignKey(NamedAttributeWorkflow)
    


    
    