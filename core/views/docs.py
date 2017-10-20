import json

from django.http import HttpResponse

from core.errors_code import errors
from core.models.notifications import notification_doc as notifs

def error_doc(request):
    return HttpResponse(
        '<html><body><pre><code>'
        + json.dumps(errors, indent=4, sort_keys=True)
        + '</code></pre></body></html>'
    )


def notification_doc(request):
    return HttpResponse(
        '<html><body>'
        + '''
        <h2>Intro</h2>
        you can user <b>newNotificationCount</b> in quering personType to achieve number of not seen notifications
        
        <pre><code>
        {
          teacher{
            id
            firstName
            lastName
            newNotificationCount
          }
        }
        </code></pre>
        
        also "notifications" in available in root Query,<br>
        for each notification type, relatedIds , related_text is different and is described below,<br>
        relatedIds is a comma separated string of ids of related objects to this notification<br>
        you may use it kile this:
        
        <pre><code>
        {
            notifications{
                id
                typeCode
                relatedIds
                relatedText
                timePassed
            }
        }
        </code></pre>
        
        
        to make a notification seen you need to user it's related mutation:
        
        <pre><code>
        mutation{
            makeNotificationSeen(data:{notificationId:10}){
                id
                shamsiDate
            }
        }
        </code></pre>
        you may get the data that you want in replace for id, shamsiDate
        
        
        
        <h2>notification Type description</h2>
        '''
        + '<pre><code>'
        + json.dumps(notifs, indent=4, sort_keys=True)
        + '</code></pre></body></html>'
    )
