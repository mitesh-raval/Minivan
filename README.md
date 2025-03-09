*******************************************
# Minivan README
*******************************************

A simple minifier script written using python3 for minifying vanilla javascript and css file.
Hence the name is a reverse portmanteau of 'Vanilla' and 'Minifier'.

Requires: Python >= 3.10

*******************************************
Usage Info :
*******************************************
From CLI :
   python3 minivan.py -h 

Importing as a module in a python script:
   import minivan

   def some_func():
      minivan.minify(src_file, dest_file)


*******************************************
Purpose :
*******************************************
Especially useful for developers not using any frameworks and just needing a simple minifier
for vanilla JS / CSS / HTML files without any other complex features or bundling etc. While this 
python script works on one file at a time, there are two ways to automate the minification 
of multiple files:

1) A shell script can be used to automate the task for multiple files

2) A python script that imports it as a library (see Usage Info above for more details)


*******************************************
LIMITATIONS :
*******************************************
- Variable names or function names are not shortened in the current version.


*******************************************
NOTES :
*******************************************
While, the author has tested and used this quite well, it might not account for all the 
possible caveats of code written in JS or CSS. 

Following are supported for most common possibilities :

1) Extra spaces before and after the line of code and any newlines or tabs are removed.

2) Both single line comments with '//' and multiline comments with /* .... */ are removed.

3) Inline comments are removed without affecting the code within a line, even if the comment
   is embedded within code statements. For e.g.
      
      if( /\* some comment \*/ condition) ==> if(condition)
      
4) For single line else statements without curly braces, an extra space is added after the
   keyword 'else' in javascript. So following ARE accounted for:

    CASE A:   
    
              if(condition)
  
                statement;
              
              else
                 
                statement;

    CASE B:   

              if(condition) {
                
                statement;
              
              } else
                  
                statement;

5) Any lines with '/' operator in javascript are accurately curated of comments.
   
   For e.g.:
        
        result = var1 / var2;  // some comment ==> result = var1 / var2;
        
        result = var1 / var2;  /\* some comment \*/ ==> result = var1 / var2;

*********************************************************************************************
