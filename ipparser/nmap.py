import xml.sax

class NmapParseXML(xml.sax.handler.ContentHandler):
    def __init__(self):
        self.host       = False
        self.port       = False
        self.list_hosts = []

    def init_newHost(self):
        self.host      = {'status' : '',
                          'hosts'  : [],
                          'ports'  : [],
                        }

    def init_newHostname(self):
        self.hostname  = {
                         'name' : '',
                         'type' : '',
                        }

    def init_newPort(self):
        self.port      = {
                         'portid'   : '',
                         'protocol' : '',
                         'state'    : '',
                        }

    def startElement(self, tag, attributes):
        if tag == 'host':
            self.host = True
            self.init_newHost()

        if self.host:
            if tag == 'status':
                self.host['status'] = attributes['state']

            elif tag == 'hostname':
                self.init_newHostname()
                self.hostname['name'] = attributes['name']
                self.hostname['type'] = attributes['type']

            elif tag == 'address':
                self.init_newHostname()
                self.hostname['name'] = attributes['addr']
                self.hostname['type'] = attributes['addrtype']

            elif tag == 'port':
                self.init_newPort()
                self.port['portid'] = attributes['portid']
                self.port['protocol'] = attributes['protocol']

            elif tag == 'state':
                self.port['state'] = attributes['state']

    def characters(self, content):
        return

    def endElement(self,tag):
        if tag == 'host':
            self.list_hosts.append(self.host)
            self.host = False

        elif tag == 'hostname' or tag == 'address':
            self.host['hosts'].append(self.hostname)

        elif tag == 'port':
            self.host['ports'].append(self.port)

def parse_nmap(filename, open_ports):
    output = []

    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    Handler = NmapParseXML()
    parser.setContentHandler(Handler)
    parser.parse(filename)

    for host in Handler.list_hosts:
        if host['status'] == 'up':
            for target in host['hosts']:
                if target['type'] == 'ipv4':
                    a = target['name']
                    if open_ports:
                        for port in host['ports']:
                            if port['state'] == 'open':
                                output.append("{}:{}".format(a, port['portid']))
                    else:
                        output.append(a)

    return output



