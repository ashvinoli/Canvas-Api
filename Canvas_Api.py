import requests
import json
import re

MY_AUTH_TOKEN = "Your-authentication-token-here"
COURSE_ID = "Your-course-id"

class canvas_page():
    """
    @brief      It's a canvas page data that can manipulate canvas pages using canvas API

    @details        def __init__(self,page_title,course_id)
    """
    global MY_AUTH_TOKEN
    auth_token = MY_AUTH_TOKEN
    auth_header={"Authorization": f"Bearer {MY_AUTH_TOKEN}"}
    site = "canvas.instructure.com"
    
    def __init__(self,page_title,course_id):
        self.page_title = page_title
        self.course_id = course_id
        self.page_url = canvas_page.conv_page_title_to_url(self.page_title)

    @staticmethod  
    def conv_page_title_to_url(page_title):
        """
        @brief      Converts page_title to canvas compatible url

        @details    

        @param      page_title

        @return     string
        """
        temp = ""
        pieces = re.split(" |,",page_title)
        new_assembled_title = "-".join(pieces)
        for character in new_assembled_title:
            if character==".":
                temp+="-dot-"
            elif character=="/":
                temp+="-slash-"
            else:
                temp+=character.lower()
        return temp
                
    def create_page(self,body):
        """
        @brief      Creates a canvas page

        @details    

        @param      self

        @return     None
        """
        url = f"https://{self.site}/api/v1/courses/{self.course_id}/pages"
        data = {"wiki_page[title]":self.page_title,"wiki_page[body]":body}
        my_request = requests.post(url, data=data, headers=self.auth_header)
        print(my_request.content)

    def delete_page(self):
        url = f"https://{self.site}/api/v1/courses/{self.course_id}/pages/{self.page_url}"
        my_request = requests.delete(url, headers=self.auth_header)
        print(my_request.content)

    def update_page(self,new_body):
        url = f"https://{self.site}/api/v1/courses/{self.course_id}/pages/{self.page_url}"
        data = {"wiki_page[body]":new_body}
        my_request = requests.put(url,data=data, headers=self.auth_header)
        print(my_request.content)

    def get_page_data(self):
        url = f"https://{self.site}/api/v1/courses/{self.course_id}/pages/{self.page_url}"
        my_request = requests.get(url, headers=self.auth_header)
        content = json.loads(my_request.text)
        for key in content:
            print(f"{key} => {content[key]}")
        
    def get_page_revisions(self):
        url = f"https://{self.site}/api/v1/courses/{self.course_id}/pages/{self.page_url}/revisions"
        my_request = requests.get(url, headers=self.auth_header)
        content = json.loads(my_request.text)
        print(content)
            
    @classmethod
    def list_pages(cls,course_id,page_url=""):
        """
        @brief      Returns all pages in a course_id

        @details    If page_url is provided, then it returns page corresponding to that url, else it returns all available pages upto 1000 at a time

        @param      course_id,page_url

        @return     pages in json
        """
        url = f"https://{cls.site}/api/v1/courses/{course_id}/pages/{page_url}?per_page=1000"
        my_request = requests.get(url, headers=cls.auth_header)
        if page_url=="":
            all_pages = json.loads(my_request.text)
            for elem in all_pages:
                for key in elem:
                    print(f"{key} => {elem[key]}")
                print("\n\n")
            return all_pages
        else:
            content = json.loads(my_request.text)
            for key in content:
                print(f"{key} => {content[key]}")
            return content
            

class canvas_module():
    """
    @brief      Canvas module class

    @details def __init__(self,course_id,module_name,module_id=""):
    """
    global MY_AUTH_TOKEN
    auth_token = MY_AUTH_TOKEN
    auth_header={"Authorization": f"Bearer {MY_AUTH_TOKEN}"}
    site = "canvas.instructure.com"
    allowed_module_item_types = {0:"File",1:"Page",2:"Discussion",3:"Assignment",4:"Quiz",5:"SubHeader",6:"ExternalUrl",7:"ExternalTool"}

    @classmethod
    def list_modules(cls,course_id):
        url = f"https://{cls.site}/api/v1/courses/{course_id}/modules"
        my_request = requests.get(url, headers=cls.auth_header)
        print(my_request.text)
        return json.loads(my_request.text)

    def __init__(self,course_id,module_name,module_id=""):
        self.course_id = course_id
        self.module_name = module_name
        self.module_id = module_id
        
    def get_module(self):
        url = f"https://{self.site}/api/v1/courses/{self.course_id}/modules/{self.module_id}"
        my_request = requests.get(url, headers=self.auth_header)
        print(my_request.text)

    def create_module(self):
        url = f"https://{self.site}/api/v1/courses/{self.course_id}/modules"
        data = {"module[name]":self.module_name}
        my_request = requests.post(url, data=data, headers=self.auth_header)
        print(my_request.content)
        
    def delete_module(self):
        url = f"https://{self.site}/api/v1/courses/{self.course_id}/modules/{self.module_id}"
        my_request = requests.delete(url, headers=self.auth_header)
        print(my_request.content)
        
    def get_module_items(self,item_id=""):
        url = f"https://{self.site}/api/v1/courses/{self.course_id}/modules/{self.module_id}/items/{item_id}?per_page=1000"
        my_request = requests.get(url, headers=self.auth_header)
        print(my_request.text)
        return json.loads(my_request.text)

    def create_module_item_page(self,page_url,page_indent):
        url = f"https://{self.site}/api/v1/courses/{self.course_id}/modules/{self.module_id}/items/"
        data = {"module_item[type]":"Page","module_item[indent]":page_indent,"module_item[page_url]":page_url}
        my_request = requests.post(url, data=data, headers=self.auth_header)
        print(my_request.content)
        
    

        

    
