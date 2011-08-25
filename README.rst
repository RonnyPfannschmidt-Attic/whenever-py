Whenever
=========

transcript of http://www.dangermouse.net/esoteric/whenever.html


Introduction
-------------

Whenever is a programming language which has no sense of urgency.
It does things whenever it feels like it,
not in any sequence specified by the programmer.

Design Principles
-----------------

Program code lines will always be executed,
eventually (unless we decide we don't want them to be),
but the order in which they are executed need not bear any resemblance
to the order in which they are specified.
Variables? We don't even have flow control,
we don't need no steenking variables!
Data structures? You have got to be kidding.


Language Concepts
-----------------

Since Whenever code is not necessarily executed sequentially,
lines of code become more like "to-do" lists,
which the language interpreter may tackle in any order it likes.
Since this makes it hard to ensure that certain required things have
actually been done before you do something else that relies on them,
there are language constructs to re-assign activities to the to-do list
if the pre-requisites have not yet been carried out.

Line Numbers
------------

Like most to-do lists, the lines of code in a Whenever program are numbered.
Unlike other languages with mandatory line numbers,
the line numbers do not specify the sequence in which the lines are executed,
and neither is there a GOTO statement or any equivalent.
Line numbers must be positive integers.
Line numbers need not be assigned in any particular order,
but they must be unique.

Program Execution
-----------------

A Whenever program is executed by a language interpreter
(hey, if you want to try writing a compiler for this, go right ahead).
It takes the program code and treats each line as an item in a to-do list.
The interpreter chooses an item from the list at random,
with equal probability, to execute, and executes the statement.
In some cases, the statement will contain a clause
that specifies that it cannot be executed until certain conditions apply.
This results in the statement being deferred and placed back on the to-do list.
Sometimes the statement contains a clause specifying that it be executed,
but also remain on the to-do list for further execution
until some condition applies.
And sometimes the statement can simply be executed and
removed from the to-do list.
When the interpreter is finished with a statement,
it chooses another at random from the to-do list.
When the to-do list is empty, the program halts.

Syntax Elements
---------------

Whenever is basically a simple C-like language with
no flow control functionality and no variables.
It does however have some specialised statements
to deal with the unpredictable nature of the execution environment.
Whenever is case-sensitive.

Strings
-------

String literals may be specified between double-quotes.
However, since there are no variables to assign strings to,
the only place this is really useful is in the print() statement.
Anywhere else a string is automatically converted to a number -
the well-formatted number that begins the string or zero
if no such number begins the string.

Operators and Expressions
-------------------------

The following standard mathematical and boolean operators work as expected:
`+, -, *, /, &&, ||, !`.

Arithmetic and logical expressions are constructed as usual.
Any floating point arithmetic expression in an integer context
is treated as if truncated (rounded towards zero).
Numbers and booleans in a string context are converted to strings.
The plus sign doubles as a string concatenation operator.
Increment, decrement and assignment operators do not exist,
since there are no variables for them to operate on.

Line Numbers as Booleans
-------------------------

An integer used in a boolean context evaluates to false
if the line of that number is not currently on the to-do list
and to true if it is on the to-do list at least once.
Note that non-positive integers always evaluate to false.

Simple Statements
-----------------

A valid line of code is structured as follows::

  line-number statement;

The following are valid simple statements:

Line Numbers
  An expression which evaluates to a positive integer
  is an instruction to submit the line with that number
  to the to-do list. A single line may appear on the to-do list
  multiple times because of this,
  and each instance must be executed separately.
  An expression which evaluates to a negative integer is an instruction
  to remove the line with the absolute value of that number from the to-do list.
  If the line in question is not on the to-do list, nothing happens.
  If it is on the to-do list multiple times, one copy is removed.
  The integer zero does nothing, but is legal syntax.
  Multiple line numbers may be specified, separated by commas.
  To specify the same number many times the shorthand notation

line-number#number-of-times-to-add/remove
  may be used. The number-of-times-to-add/remove may be any expression which evaluates to an integer,
  a negative number of times corresponds to changing the sign of the line number, and zero does nothing.::

      1 4,5#3,-6;

Input
------
A basic read statement reads from STDIN.
read() reads a variable amount of data - if the data form a number,
it reads to the end of the number and returns that number.
If the first character it reads is non-numeric, it returns the Unicode numeric value of that character.

::

  1 2#read();

Output
------

A basic print statement prints to STDOUT. There is no fancy formatting,
and it only takes one string argument. It automatically appends a newline.

::

  1 print("Hi there");

Compound Statements
-------------------

Compound statements contain some conditional or repetitive clause
which causes a statement to be executed conditonally.

defer

  line-number defer (boolean) statement;
  The defer statement takes a boolean argument.
  If the argument is true, the statement is deferred - i.e.
  the remainder of the statement is not executed and
  the line number of the defer statement remains on the to-do list.

  ::

    1 defer (2) 3;

again

  line-number again (boolean) statement;
  The again statement takes a boolean argument.
  If the argument is true, the statement is executed
  but remains on the to-do list,
  to be executed again some time later.
  If the argument is false, the statement is executed and
  removed from the to-do list as normal.

  ::

    1 again (2) 3;

forget (deprecated)

  line-number forget (boolean) statement;
  The forget statement takes a boolean argument. If the argument is true, the statement is forgotten - it is not executed but is removed from the to-do list. If the argument is false, the statement is executed and removed from the to-do list as normal.

  ::

    1 forget (2) 3;

  forget is deprecated because the same functionality can be achieved as follows (and I'm not sure what use this statement is anyway):

  ::

    1 defer (4 && !2) 3;
    4 defer (2) -1;

Combinations of compound statements
-----------------------------------

The statement in a compound statement structure may be a compound statement.
If any defer argument is true, the entire statement is deferred.
If any again argument is true, the statement remains on the to-do list (whether it is actually executed or not).
In practice a single again and single defer clause cover all possibilities (and the order is unimportant),
so long chains of multiple agains and defers are unnecessary.

Built-in Functions
-------------------
Most standard mathematical functions (trigonometry, etc) are supported, plus the following:

N()
  takes an integer argument and returns the number of times that line number is in the current to-do list.

U()
  takes an integer argument and returns a string containing the Unicode character with that Unicode number.
  This is mostly useful inside print() statements, but may be useful elsewhere
  (where the string will immediately be converted back to a number - zero unless the Unicode character is a digit).

Sample Programs
---------------

Hello World
+++++++++++

This is actually embarrassingly trivial in Whenever. Sort of a shame when you see it done in languages like Befunge and Malbolge.

::

  1 print("Hello world!");

Endless Loop
++++++++++++
This program simply sets up an endless loop and will never terminate. It is also the shortest valid program in Whenever.

::

  1 1;

Memory Hog
++++++++++

This will do the same thing as the endless loop, but will accumulate multiple copies of the line in the interpreter's to-do list and eventually grind your computer to a halt as it runs out of RAM. An extra character or two will make your machine run out of memory in an exponentially faster time. What fun!

::

  1 1#9;

99 Bottles of Beer
++++++++++++++++++

Something more interesting.

::

  1 defer (4 || N(1)<N(2) && N(2)<N(3)) print(N(1)+" bottles of beer on the wall, "+N(1)+" bottles of beer,");
  2 defer (4 || N(1)==N(2)) print("Take one down and pass it around,");
  3 defer (4 || N(2)==N(3)) print(N(1)+" bottles of beer on the wall.");
  4 1#98,2#98,3#98;

Fibonacci Numbers
+++++++++++++++++

This prints the first 100 Fibonacci numbers. Eventually.

::

  1 again (1) defer (3 || N(1)<=N(2) || N(7)>99) 2#N(1),3,7;
  2 again (2) defer (3 || N(2)<=N(1) || N(7)>99) 1#N(2),3,7;
  3 defer (5) print(N(1)+N(2));
  4 defer (5) print("1");
  5 4,-3,7;
  6 defer (4) 3;
  7 7;
  8 defer (N(7)<100) -1#N(1),-2#N(2),-7#100,-3;
  9 defer (3 || 6) 1,3;
