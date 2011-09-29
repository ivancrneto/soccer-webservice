from soaplib.core.service import DefinitionBase, soap
from soaplib.core.model.primitive import String, Integer, Any
from xml.dom import minidom

from futebol.service.models import XmlEvent


class WebService(DefinitionBase):
    '''
    The actual webservice class.
    This defines methods exposed to clients.
    '''
    def __init__(self, environ):
        '''
        This saves a reference to the request environment on the current instance
        '''
        self.environ = environ
        super(WebService, self).__init__(environ)

    @soap(String, _returns=String)# Soap is typed - we need stuff like this
    def hello_soap_world(self, name):
        return "Hello, %s!" % name
    
    @soap(Integer, _returns=Any)
    def get_events(self, last_id):
        dir(last_id)
        events = XmlEvent.objects.filter(id__gt=last_id)
        data = "<events>"
        for event in events:
            data += "<event>"    
            data += "<id>" + str(event.id) + "</id>"
            data_doc = minidom.parseString(event.data.encode('utf-8'))
            type_tag = data_doc.getElementsByTagName("type")
            timestamps_tag = data_doc.getElementsByTagName("timestamps")
            data += timestamps_tag[0].toxml()
            data += type_tag[0].toxml()
            event_data = data_doc.getElementsByTagName("data")
            data += event_data[0].toxml()
            data += "</event>"
        data += "</events>"
        return data
