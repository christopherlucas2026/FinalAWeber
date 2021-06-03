from models.widget import WidgetModel


def test_new_widget():
    widget = WidgetModel("scuddler", 6)
    assert widget.name == "scuddler"
    assert widget.parts == 6
