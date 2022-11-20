*********************************************************************************************
# Minivan README
*********************************************************************************************

A simple minifier script written using python3 for minifying vanilla javascript and css file.
Hence the name is a reverse portmanteau of 'Vanilla' and 'Minifier'.

   WARNING : Multiple embedded comments within a single line of code are NOT handled. Please
             see LIMITATIONS AND WARNINGS for more details !

*******************************************
python3 minivan.py -h will display usage.
*******************************************

*******************************************
Purpose :
*******************************************
Especially useful for developers not using any frameworks and just needing a simple minifier
for vanilla JS and CSS files without any other complex features or bundling etc. This script 
only works on one file at a time, but a shell script can be used to automate the task for 
multiple files. That is out of scope for this minifier, as each developer might have 
different dir structures etc.

*******************************************
LIMITATIONS AND WARNINGS :
*******************************************
While, the author has tested and used this quite well, it might not account for all the 
possible caveats of code written in JS or CSS. 
Following are supported for most common possibilities :
1) Extra spaces before and after the line of code and any newlines or tabs are removed.

2) Both single line comments with '//' and multiline comments with /* .... */ are removed.

3) Inline comments are removed without affecting the code within a line, even if the comment
   is embedded within code statements. For e.g.
      if( /\* some comment \*/ condition) ==> if(condition)
   WARNING : However, multiple embedded comments within a single line of code are NOT handled.
      For e.g.  if(/\* comment 1 \*/ condition) /\* comment 2 \*/  ==> SYNTAX error

4) For single line else statements without curly braces, an extra space is added after the
   keyword 'else' in javascript. So following are accounted for:

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

5) Any lines with http:// or https:// as preserved AS IS.

6) Any lines with '/' operator in javascript are accurately curated of comments.
   
   For e.g.:
        
        result = var1 / var2;  // some comment ==> result = var / var2;
        
        result = var1 / var2;  /\* some comment \*/ ==> result = var / var2;

*********************************************************************************************
