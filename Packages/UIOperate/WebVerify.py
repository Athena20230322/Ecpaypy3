from UIOperate import WebOperate
import LibGeneral.TestHelper as Thelper


class webVerification():
    def __init__(self, input_drv, elem_list_csvpath, log_file_relat_path):

        self.drv = input_drv
        self.helper = Thelper.classTestHelper(log_file_relat_path)
        self.identds = self.helper.generateElemDataset(elem_list_csvpath)

        
    def test(self):
        self.drv.get('https://www.google.com')
        
    def verifyElem(self, elem_ident, find_by='id'):
        if find_by == 'id':
            elem = self.drv.find_element_by_id(elem_ident)
        elif find_by == 'class':
            elem = self.drv.find_element_by_class_name(elem_ident)
        elif find_by == 'css':
            elem = self.drv.find_element_by_css_selector(elem_ident)
        else:
            err_msg = "verifyElem: Specified 'findby' argument is not correct."
            raise ValueError(err_msg)
        
        if elem.location != None:
            #elem.click()
            #print 'Clicked'
            return True
        else:
            return False
        
    def verifyMultipleElems(self, *Elem_alais):
        get = self.helper.getElemIdentFromDataSet
        ids = self.identds
        result_dict = {}
        for n in Elem_alais:
            logout_ident = get(n, ids)
            result = self.verifyElem(logout_ident['Identifier'], logout_ident['Element_type']) 
            result_dict[n] = result
            
        return result_dict
            
    def verifyHTMLTableContent(self, tb_elem, value, typ='data', partial=False):
        if typ == 'data':
            by = 'td'
        elif typ == 'row':
            by = 'tr'
        elif typ == 'header':
            by = 'th'
            
        tb_objs = tb_elem.find_elements_by_tag_name(by)
        if partial is False:
            search_res = {x.text.encode('big5') : tb_objs.count(x) for x in tb_objs if x.text.encode('big5') == value}
        #elif partial is True:
            #search_res = {x : tb_objs.count(x) for x in tb_objs if x.__contains__(value) is True}
            
        return search_res
    
    def verifyAlert(self, msg, action='Accept'):
        pass