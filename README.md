# store-parser
A python3 library that queries product prices in popular online stores.

<h2>How it works</h2>
<p>
   It connects to online store websites using HTTP GET and parses the markup using lxml (https://github.com/lxml/lxml). Each store parser placed under the plugins directory is loaded at runtime and called to extract product information.
</p>
<p>
   The sequence of steps is controlled by the Parser super class as described below:
</p>
<ul>
   <li>An initial request using the supplied term is performed, to extract the page count of the results</li>
   <li>For every page, a separate request is made to extract the list of products</li>
   <li>The results from all stores are added to a unified list and returned to the caller</li>
</ul>

<h2>Installation</h2>
<h4>Prerequisites</h4>
<ul>
   <li>Requires python 3+</li>
   <li>Requires lxml -> pip3 install lxml</li>
</ul>
<h4>Usage</h4>
<p>
```
python3 store-parser -q "marshall amp"
```
</p>

<h2>Adding support for other stores</h2>
<h4>Steps</h4>
<ul>
   <li>Add your [store-name-in-lowercase].py in the plugins directory</li>
   <li>Write a class that inherits from Parser named by this convention: [Store-name-capitalized]Parser</li>
   <li>
      In your <b>__init__</b> method call the super class __init__ using (name, host, path, key_query, key_page) where:
      <ul>
         <li>name is the name of the plugin - only used for logging purposes</li>
         <li>host is the domain of the store, eg. <b>mystore.com</b></li>
         <li>path is the relative path of the search page, eg. <b>/search?</b></li>
         <li>key_query is the query string key used for the search term, eg. search?<b>keywords=tube+screamer</b></li>
         <li>key_page is the query string key used for the result page, eg. search?keywords=tube+screamer&<b>page=2</b></li>
      </ul>
   </li>
</ul>
   
```python
from parsing import Parser, HtmlTraversal
from query import Result


class MyStoreParser(Parser):
    def __init__(self):
        super().__init__("mystore", "www.mystore.com", "/search?lang=en", "keywords", "page")

    def extract_page_count(self, markup):
        count = 1

        traverse = HtmlTraversal(markup)
        elements = traverse.get_elements("a", {"class": "page last"})

        if len(elements) > 0:
            count = int(traverse.in_element(elements[-1]).get_value())

        return count

    def extract_results(self, markup):
        results = []

        traverse = HtmlTraversal(markup)
        elements = traverse.get_elements("li", {"class": "result"})

        for x in elements:
            result = Result()
            result.title = traverse.in_element(x).get_value_of("a", {"class": "title"})
            result.url = traverse.in_element(x).get_attr_of("a", {"class": "title"}, "href")
            result.price = traverse.in_element(x).get_value_of("span", {"class": "price"})
            results.append(result)

        return results
```

<h2>Contribution</h2>
<p>
    Contributions for new features and support for new stores are very welcome. The only requirements are that the code is clean, readable and conforms to PEP 8 - coding style guide for python.
</p>
