import re
import textwrap

import factory
from factory.django import DjangoModelFactory

from .models import CodeSample

from users.factories import UserFactory


class CodeSampleFactory(DjangoModelFactory):

    class Meta:
        model = CodeSample
        django_get_or_create = ('code',)

    creator = factory.SubFactory(UserFactory)
    code = factory.Faker('sentence', nb_words=10)
    code_markup_type = 'html'
    copy = factory.Faker('sentence', nb_words=10)
    copy_markup_type = 'html'
    is_published = True


def initial_data():
    def format_html(code):
        """Add HTML tags for highlighting of the given code snippet."""
        code = code.strip()
        for pattern, repl in [
            (r'^([^\s\.>#].*)$', r'<span class="output">\1</span>'),
            (r'^(>>>)', r'<span class="code-prompt">\1</span>'),
            (r'^(\.\.\.)', r'<span class="code-prompt">\1</span>'),
            (r'(#.*)$', r'<span class="comment">\1</span>'),
        ]:
            code = re.sub(pattern, repl, code, flags=re.MULTILINE)
        return f'<pre><code>{code}</code></pre>'

    code_samples = [
        (
            r"""
            # Simple output (with Unicode)
            >>> print("Hello, I'm Python!")
            Hello, I'm Python!

            # Input, assignment
            >>> name = input('What is your name?\n')
            >>> print('Hi, %s.' % name)
            What is your name?
            Python
            Hi, Python.
            """,
            """\
            <h1>Quick &amp; Easy to Learn</h1>
            <p>Experienced programmers in any other language can pick up Python very
            quickly, and beginners find the clean syntax and indentation structure
            easy to learn.
            <a href=\"https://docs.python.org/3/tutorial/\">Whet your appetite</a>
            with our Python overview.</p>
            """
        ),
        (
            """
            # Simple arithmetic
            >>> 1 / 2
            0.5
            >>> 2 ** 3
            8
            >>> 17 / 3  # true division returns a float
            5.666666666666667
            >>> 17 // 3  # floor division
            5
            """,
            """\
            <h1>Intuitive Interpretation</h1>
            <p>Calculations are simple with Python, and expression syntax is
            straightforward: the operators <code>+</code>, <code>-</code>,
            <code>*</code> and <code>/</code> work as expected; parentheses
            <code>()</code> can be used for grouping.
            <a href=\"https://docs.python.org/3/tutorial/introduction.html
            #using-python-as-a-calculator\">More about simple math functions</a>.
            </p>
            """
        ),
        (
            """
            # List comprehensions
            >>> fruits = ['Banana', 'Apple', 'Lime']
            >>> loud_fruits = [fruit.upper() for fruit in fruits]
            >>> print(loud_fruits)
            ['BANANA', 'APPLE', 'LIME']

            # List and the enumerate function
            >>> list(enumerate(fruits))
            [(0, 'Banana'), (1, 'Apple'), (2, 'Lime')]
            """,
            """\
            <h1>Compound Data Types</h1>
            <p>Lists (known as arrays in other languages) are one of the
            compound data types that Python understands. Lists can be indexed,
            sliced and manipulated with other built-in functions.
            <a href=\"https://docs.python.org/3/tutorial/introduction.html
            #lists\">More about lists</a></p>
            """
        ),
        (
            """
            # For loop on a list
            >>> numbers = [2, 4, 6, 8]
            >>> product = 1
            >>> for number in numbers:
            ...     product = product * number
            ...
            >>> print('The product is:', product)
            The product is: 384
            """,
            """\
            <h1>All the Flow You&rsquo;d Expect</h1>
            <p>Python knows the usual control flow statements that other
            languages speak &mdash; <code>if</code>, <code>for</code>,
            <code>while</code> and <code>range</code> &mdash; with some of
            its own twists, of course.
            <a href=\"https://docs.python.org/3/tutorial/controlflow.html\">
            More control flow tools</a></p>
            """
        ),
        (
            """
            # Write Fibonacci series up to n
            >>> def fib(n):
            >>>     a, b = 0, 1
            >>>     while a &lt; n:
            >>>         print(a, end=' ')
            >>>         a, b = b, a+b
            >>>     print()
            >>> fib(1000)
            0 1 1 2 3 5 8 13 21 34 55 89 144 233 377 610
            """,
            """\
            <h1>Functions Defined</h1>
            <p>The core of extensible programming is defining functions.
            Python allows mandatory and optional arguments, keyword arguments,
            and even arbitrary argument lists.
            <a href=\"https://docs.python.org/3/tutorial/controlflow.html
            #defining-functions\">More about defining functions</a></p>
            """
        ),
    ]
    return {
        'boxes': [
            CodeSampleFactory(
                code=format_html(textwrap.dedent(code)),
                copy=textwrap.dedent(copy),
            ) for code, copy in code_samples
        ],
    }
