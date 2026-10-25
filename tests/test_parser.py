from stacktrace_doctor.parser import parse

TRACE = """org.springframework.beans.factory.UnsatisfiedDependencyException: Error creating bean 'orderController'
\tat org.springframework.beans.factory.support.ConstructorResolver.createArgumentArray(ConstructorResolver.java:795)
Caused by: org.springframework.beans.factory.NoSuchBeanDefinitionException: No qualifying bean of type 'OrderService'
\tat org.springframework.beans.factory.support.DefaultListableBeanFactory.raiseNoMatchingBeanFound(X.java:1880)
\t... 19 common frames omitted"""


def test_deepest_cause_is_last():
    p = parse(TRACE)
    assert p is not None
    assert p.root.type.endswith("NoSuchBeanDefinitionException")
    assert len(p.chain) == 2


def test_detects_spring():
    assert "Spring Framework" in parse(TRACE).frameworks


def test_not_a_trace_returns_none():
    assert parse("hello world") is None
    assert parse("") is None


def test_stack_frames_are_not_exceptions():
    p = parse(TRACE)
    assert all(not e.type.startswith("at ") for e in p.chain)


def test_message_with_colons_is_kept_whole():
    p = parse("java.lang.IllegalStateException: Failed: reason: timeout at 10:15")
    assert p.root.message == "Failed: reason: timeout at 10:15"


def test_exception_in_thread_main():
    p = parse('Exception in thread "main" java.lang.NullPointerException: Cannot invoke "String.length()"')
    assert p.root.type == "java.lang.NullPointerException"


def test_exception_without_message():
    p = parse("java.util.ConcurrentModificationException\n\tat java.base/java.util.ArrayList$Itr.next(X.java:1)")
    assert p.root.type == "java.util.ConcurrentModificationException"
    assert p.root.message == ""


def test_windows_line_endings():
    p = parse(TRACE.replace("\n", "\r\n"))
    assert p.root.type.endswith("NoSuchBeanDefinitionException")


def test_log_lines_before_the_trace_are_ignored():
    text = (
        "2026-10-20T10:15:30.123+05:30 ERROR 1 --- [main] o.s.boot.SpringApplication : Application run failed\n" + TRACE
    )
    assert len(parse(text).chain) == 2


def test_spring_resolved_log_line():
    line = (
        "WARN 1 --- [nio-8080-exec-1] .w.s.m.s.DefaultHandlerExceptionResolver : Resolved "
        "[org.springframework.http.converter.HttpMessageNotReadableException: JSON parse error: Unexpected character]"
    )
    p = parse(line)
    assert p.root.type.endswith("HttpMessageNotReadableException")
    assert p.root.message.startswith("JSON parse error")


def test_nested_class_exception():
    p = parse(
        "org.springframework.boot.autoconfigure.jdbc.DataSourceProperties$DataSourceBeanCreationException: "
        "Failed to determine a suitable driver class"
    )
    assert p.root.simple_name == "DataSourceProperties$DataSourceBeanCreationException"


def test_duplicate_root_cause_is_not_repeated():
    text = (
        TRACE
        + "\n"
        + "org.springframework.beans.factory.NoSuchBeanDefinitionException: No qualifying bean of type 'OrderService'"
    )
    assert len(parse(text).chain) == 2


def test_suppressed_exceptions_are_ignored():
    text = "java.io.IOException: disk full\n\tSuppressed: java.lang.IllegalStateException: close failed"
    p = parse(text)
    assert [e.type for e in p.chain] == ["java.io.IOException"]


def test_long_messages_are_truncated():
    p = parse("java.lang.RuntimeException: " + "x" * 2000)
    assert len(p.root.message) == 500
