from ebooklib import epub
import os
import re


def sort_custom(x):
    res = re.findall(r'\d+', x)
    return int(res[0])



def create_book(name):
    print(name)
    book = epub.EpubBook()

    book.set_identifier('5646546')
    book.set_title(name.replace("_"," "))
    book.set_language('en')

    files = os.listdir(os.getcwd())
    if any(".epub" in x for x in files):
        files.remove(f"{name}.epub")
    
    files= sorted(files,key=sort_custom)
    content = []

    for file in files:

        if file[-5:]!=".text":
            continue
        with open(file , "r",encoding="utf-8") as f :
            c = epub.EpubHtml(title=file[:-5], file_name=f'{file[:-5]}.xhtml', lang='en')
            c.content=""
            c.content+=f'<h2>{file[:-5]}</h2>'
            for line in f.readlines():
                c.content+=f'<p>{line}</p>'
        
        book.add_item(c)
        content.append(c)
        book.toc.append(epub.Link(f'{file[:-5]}.xhtml', file[:-5], "id"+file[:-5]))
    

    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    style = '''
@namespace epub "http://www.idpf.org/2007/ops";
body {
    font-family: Cambria, Liberation Serif, Bitstream Vera Serif, Georgia, Times, Times New Roman, serif;
}
h2 {
     text-align: left;
     text-transform: uppercase;
     font-weight: 200;     
}
ol {
        list-style-type: none;
}
ol > li:first-child {
        margin-top: 0.3em;
}
nav[epub|type~='toc'] > ol > li > ol  {
    list-style-type:square;
}
nav[epub|type~='toc'] > ol > li > ol > li {
        margin-top: 0.3em;
}
'''

    nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
    book.add_item(nav_css)

    book.spine = ['nav', *content]

    epub.write_epub(f'{name}.epub', book, {})
