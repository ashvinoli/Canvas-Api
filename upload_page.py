import Canvas_Api

def create_all_modules(module_list_file):
    """
    @brief      It creates modules from the file given

    @details    By taking each line of the file as the name of new module this function creates modules in the canvas site.

    @param      FILE

    @return     None
    """
    with open(module_list_file,"r") as modules:
        for line in modules.readlines():
            temp_module = Canvas_Api.canvas_module(Canvas_Api.COURSE_ID,line.strip())
            temp_module.create_module()

def delete_all_modules(module_list_file):
    """
    @brief      It deletes modules in a given file

    @details    By taking the lines in the given file as names of module, it deletes all the matching modules from the canvas site.

    @param      module_list_file

    @return     None
    """
    with open(module_list_file,"r") as modules:
        modules_list = Canvas_Api.canvas_module.list_modules(Canvas_Api.COURSE_ID)
        for line in modules.readlines():
            temp_module = Canvas_Api.canvas_module(Canvas_Api.COURSE_ID,line.strip())
            for module in modules_list:
                if temp_module.module_name==module["name"]:
                    temp_module.module_id = str(module["id"])
                    temp_module.delete_module()
                    break
                

def increase_middle_number(line):
    """
    @brief      It alters the numberings of chapters

    @details    If you provide it 3.1 or 3.1.2 it will change it to 3.2 or 3.2.2 i.e it increments second dot 

    @param      line

    @return     string
    """
    tokens = line.strip().split()
    splitted = tokens[0].split(".")
    splitted[1]=str(int(splitted[1])+1)
    merged = ".".join(splitted)
    tokens[0] = merged
    new_line = " ".join(tokens)
    return new_line

def create_all_pages(page_file):
    """
    @brief      It creates pages.

    @details    By taking the lines in the given file as pages' name it creates all given pages in the canvas site.

    @param      page_file

    @return     None
    """
    with open(page_file,"r") as pages:
        for line in pages.readlines():
            new_line = increase_middle_number(line)
            temp_page = Canvas_Api.canvas_page(new_line,Canvas_Api.COURSE_ID)
            temp_page.create_page("")

def delete_all_pages(page_file):
    """
    @brief      It deletes page_files

    @details    By taking the lines in the given file as name of page to be deleted, this functions deletes all the matching names.

    @param      page_file

    @return     None
    """
    with open(page_file,"r") as pages:
        pages_list = Canvas_Api.canvas_page.list_pages(Canvas_Api.COURSE_ID)
        for line in pages.readlines():
            new_line = increase_middle_number(line)
            temp_page = Canvas_Api.canvas_page(new_line,Canvas_Api.COURSE_ID)
            for page in pages_list:
                if temp_page.page_title==page["title"]:
                    temp_page.page_url = page["url"]
                    temp_page.delete_page()
                    break
            
def assign_pages_to_modules():
    """
    @brief      It maps modules to pages

    @details    By reading all modules and all pages, this function groups them i.e forms a dictionary of module_id and page_url list by comparing the first number that starts their names i.e 1. Ram will map to all 1.1 1.2 1.3 or whatever chapters there are. The data are downloaded from the canvas site and mapped

    @param      None

    @return     Dictionary of module_ids=>list of page_urls
    """
    modules_list = Canvas_Api.canvas_module.list_modules(Canvas_Api.COURSE_ID)
    pages_list = Canvas_Api.canvas_page.list_pages(Canvas_Api.COURSE_ID)
    page_map = {}
    for module in modules_list:
        module_number = module["name"].split(".")[0]
        page_map[str(module["id"])] = []
        for page in pages_list:
            page_number = page["title"].split(".")[0]
            if module_number==page_number:
                page_map[str(module["id"])].append(page["url"])
    return page_map

def put_pages_inside_modules():
    """
    @brief      This actually implements the module_id=>list of page_url map

    @details    By using the map generated, it places all the relevant pages inside relevant module in the canvas site.

    @param      None

    @return     None
    """
    page_map = assign_pages_to_modules()
    for mod_id in page_map:
        temp_module = Canvas_Api.canvas_module(Canvas_Api.COURSE_ID,"Who_Cares",mod_id)
        module_items = temp_module.get_module_items()
        for page_url in page_map[mod_id]:
            present = False
            for module_item in module_items:
                if module_item["type"]=="Page":
                    if module_item["page_url"]==page_url:
                        present = True
                        break
            if not(present):
                temp_module.create_module_item_page(page_url,1)
        



