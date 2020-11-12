from pathlib import Path

from ploomber import DAG
from ploomber.tasks import PythonCallable
from ploomber.products import File, MetaProduct


def touch_all(product):
    for p in product:
        Path(str(p)).touch()


def touch_all_upstream(product, upstream):
    for p in product:
        Path(str(p)).touch()


def test_get():
    a = File('1.txt')
    m = MetaProduct({'a': a})

    assert m.get('a') is a
    assert m.get('b') is None


def test_delete_metadata(tmp_directory):
    Path('a.txt.source').touch()
    Path('b.txt.source').touch()

    a = File('a.txt')
    b = File('b.txt')
    m = MetaProduct({'a': a, 'b': b})
    m.metadata.delete()

    assert not Path('a.txt.source').exists()
    assert not Path('b.txt.source').exists()


def test_can_iterate_over_products():
    p1 = File('1.txt')
    p2 = File('2.txt')
    m = MetaProduct([p1, p2])

    assert set(m) == {p1, p2}


def test_can_iterate_when_initialized_with_dictionary():
    p1 = File('1.txt')
    p2 = File('2.txt')
    m = MetaProduct({'a': p1, 'b': p2})

    assert set(m) == {p1, p2}


def test_can_create_task_with_more_than_one_product(tmp_directory):
    dag = DAG()

    fa = Path('a.txt')
    fb = Path('b.txt')
    fc = Path('c.txt')
    fd = Path('d.txt')

    ta = PythonCallable(touch_all, (File(fa), File(fb)), dag, 'ta')
    tc = PythonCallable(touch_all_upstream, (File(fc), File(fd)), dag, 'tc')

    ta >> tc

    dag.build()

    assert fa.exists()
    assert fb.exists()
    assert fc.exists()
    assert fd.exists()
