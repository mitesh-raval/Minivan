/*! This is a multi
 * line loud 
 * comment 
 * */

/*! This is a one line loud comment */

/* this is a multi-line
*/

function some_func(some_arg) {
    urlStr = /* comment 1 */ 'http://www.example.com'; /* comment 2 */
    urlStr = 'https://www.example.com';
    console.log('test');  /* another 'hello
    world" multi line comment */
    if(blah)
        some_statement;
    else
        single_statement;
    var p ="some string"; 
    var r = `<div class='some-css-class' 
            >${p} </div>`;
    var q = 'this has /* not a comment */ within string';
    var s = ' "Hello" world \
             second hello world /* some not a comment \
             continued to the next line */ ';
}
//# ignore source map line