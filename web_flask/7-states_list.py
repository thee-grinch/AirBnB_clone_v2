<!DOCTYPE HTML>
<HTML LANG="en">
    <HEAD>
        <TITLE>HBNB</TITLE>
    </HEAD>
    <BODY>
        <H1>States</H1>
        <UL>
        {% for state in states | sort(attribute="name") %}
            <LI>{{ state.id }}: <B>{{ state.name }}</B></LI>
        {% endfor %}
    </UL>
</BODY>
</HTML>
