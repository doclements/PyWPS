"""
WPS GetCapabilities request handler
"""
# Author:	Jachym Cepicky
#        	http://les-ejk.cz
#               jachym at les-ejk dot cz
# Lince: 
# 
# Web Processing Service implementation
# Copyright (C) 2006 Jachym Cepicky
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

from Request import Request

class GetCapabilities(Request):
    """
    Parses input request obtained via HTTP POST encoding - should be XML
    file.
    """

    def __init__(self,wps):
        """
        Arguments:
           self
           wps   - parent WPS instance
        """
        Request.__init__(self,wps)

        self.template = self.templateManager.prepare(self.templateFile)

        #
        # ServiceIdentification
        #
        self.templateProcessor.set("encoding",
                                    self.wps.getConfigValue("wps","encoding"))
        self.templateProcessor.set("servertitle",
                                    self.wps.getConfigValue("wps","title"))
        self.templateProcessor.set("serverabstract",
                                    self.wps.getConfigValue("wps","abstract"))
        self.templateProcessor.set("version",
                                    self.wps.getConfigValue("wps","version"))
        self.templateProcessor.set("fees",
                                    self.wps.getConfigValue("wps","fees"))
        self.templateProcessor.set("constraints",
                                    self.wps.getConfigValue("wps","constraints"))

        #
        # ServiceProvider
        #
        self.templateProcessor.set("providername",
                            self.wps.getConfigValue("provider","providerName"))
        self.templateProcessor.set("individualname",
                        self.wps.getConfigValue("provider","individualName"))
        self.templateProcessor.set("positionname",
                            self.wps.getConfigValue("provider","positionName"))
        self.templateProcessor.set("providersite",
                            self.wps.getConfigValue("provider","providerSite"))
        # phone
        if self.wps.getConfigValue("provider","voice") or \
            self.wps.getConfigValue("provider","fascimile"):
            self.templateProcessor.set("phone", 1)
            if self.wps.getConfigValue("provider","voicephone"):
                self.templateProcessor.set("voicephone",
                                    self.wps.getConfigValue("provider","voice"))
            if self.wps.getConfigValue("provider","fascimilephone"):
                self.templateProcessor.set("fascimilephone",
                                    self.wps.getConfigValue("provider","fascimile"))
        else:
            self.templateProcessor.set("phone", 0)

        # address
        if self.wps.getConfigValue("provider","deliveryPoint") or \
           self.wps.getConfigValue("provider","city") or \
           self.wps.getConfigValue("provider","administrativeArea") or \
           self.wps.getConfigValue("provider","postalCode") or \
           self.wps.getConfigValue("provider","country") or \
           self.wps.getConfigValue("provider","electronicMailAddress"):

            self.templateProcessor.set("address", 1)
            if self.wps.getConfigValue("provider","deliveryPoint"):
                self.templateProcessor.set("deliverypoint",
                            self.wps.getConfigValue("provider","deliveryPoint"))
            if self.wps.getConfigValue("provider","city"):
                self.templateProcessor.set("city",
                            self.wps.getConfigValue("provider","city"))
            if self.wps.getConfigValue("provider","administrativeArea"):
                self.templateProcessor.set("administrativearea",
                        self.wps.getConfigValue("provider","administrativeArea"))
            if self.wps.getConfigValue("provider","postalCode"):
                self.templateProcessor.set("postalcode",
                            self.wps.getConfigValue("provider","postalCode"))
            if self.wps.getConfigValue("provider","country"):
                self.templateProcessor.set("country",
                            self.wps.getConfigValue("provider","country"))
            if self.wps.getConfigValue("provider","electronicMailAddress"):
                self.templateProcessor.set("electronicmailaddress",
                    self.wps.getConfigValue("provider","electronicMailAddress"))
        else:
           self.templateProcessor.set("address", 0)
            
        # OperationsMetadata
        self.templateProcessor.set("url",self.wps.getConfigValue("wps","serveraddress"))
        self.templateProcessor.set("Operations",
                                    [{"operation":"GetCapabilities"}, 
                                     {"operation":"DescribeProcess"},
                                     {"operation":"Execute"}])

        # Processes
        processesData = []

        # Import processes
        
        for processName in self.processes.__all__:

            processData = {}
            try:
                module = __import__(self.processes.__name__,fromlist=[processName])
                process = eval("module."+processName+".Process()")

                processData["processok"] = 1
                processData["identifier"] = process.identifier
                processData["title"] = process.title
                processData["abstract"] = process.abstract
                processData["profile"] = process.profile
                processData["wsdl"] = process.wsdl
                processData["metadatalen"] = 0
            except Exception, e:
                processData["processok"] = 0
                processData["process"] = processName
                processData["exception"] = e
            processesData.append(processData)
        self.templateProcessor.set("Processes",processesData)



        # Language
        self.templateProcessor.set("language",self.wps.getConfigValue("wps","lang"))

        self.response = self.templateProcessor.process(self.template)
        return