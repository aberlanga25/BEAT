import xmlschema
import xmltodict
import dicttoxml
import view.poi
import pop
from model import plugin
from xml.dom.minidom import parseString


class poi_tab_controller:

    def __init__(self, poi_tab):
        self.poi_tab = poi_tab
        self.poi_tab.comboBox_2.addItem("All")

    def establish_connections(self):
        self.poi_tab.comboBox.currentIndexChanged.connect(lambda x: self.fillPOIs(
            cplg=self.poi_tab.comboBox.currentText()))
        self.poi_tab.listWidget_2.itemSelectionChanged.connect(self.itemActivatedPlugin)
        self.poi_tab.comboBox_2.currentIndexChanged.connect(lambda x: self.filterPOIs(cplg=self.poi_tab.comboBox.currentText(),
                                                                             type=self.poi_tab.comboBox_2.currentText()))
        self.poi_tab.pushButton_11.clicked.connect(self.instantiateAddPOIWindow)

    def establish_calls(self):
        self.setPlugins()

    def setPlugins(self):
        for pl in plugin.getInstalledPlugins():
            self.poi_tab.comboBox.addItem(pl)

    def fillPOIs(self, cplg):
        doc = plugin.pluginConnection(cplg)
        types = []
        for i in doc["plugin"]["point_of_interest"]["item"]:
            self.poi_tab.listWidget_2.addItem(str(i["name"]))
            if i["type"] not in types:
                types.append(i["type"])
                self.poi_tab.comboBox_2.addItem(i["type"])

    def filterPOIs(self, cplg, type):
        doc = plugin.pluginConnection(cplg)
        for i in doc["plugin"]["point_of_interest"]["item"]:
            if type != "All":
                print(i)
                if i["type"] == type:
                    self.poi_tab.listWidget_2.addItem(str(i["name"]))
            else:
                self.poi_tab.listWidget_2.addItem(str(i["name"]))

    def itemActivatedPlugin(self):
        poiSelect = self.poi_tab.listWidget_2.selectedItems()
        poiName = [item.text().encode("ascii") for item in poiSelect]
        doc = plugin.pluginConnection(self.poi_tab.comboBox.currentText)
        if poiName:
            for i in doc["plugin"]["point_of_interest"]["item"]:
                if poiName[0].decode() == i["name"]:
                    self.poi_tab.textEdit.setText(i["name"] + " " + i["type"])

    def instantiateAddPOIWindow(self):
        pop = pop.addPOIDialog(self)
        text, out, type = pop.exec_()
        newpoi = {"name": text, "type": type, "pythonOutput": out}
        doc = plugin.pluginConnection(self.poi_tab.comboBox.currentText)
        pl = plugin.getPluginFile(self.poi_tab.comboBox.currentText)
        old = doc["plugin"]["point_of_interest"]["item"]
        old.append(newpoi)
        doc["plugin"]["point_of_interest"] = old
        xml = dicttoxml.dicttoxml(doc, attr_type=False, root=False)
        dom = parseString(xml)
        wr = open('plugins/%s' % pl, 'w')
        wr.write(dom.toprettyxml())
        wr.close()
        self.filterPOIs(str(self.poi_tab.comboBox.currentText()), str(self.poi_tab.comboBox_2.currentText()))