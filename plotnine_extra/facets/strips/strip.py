"""
Base strip class for facet strip labels.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any


class Strip:
    """
    Base class for facet strip labels.

    Strips are the text labels displayed above or beside facet
    panels indicating which variable values the panel represents.

    Subclass this and override :meth:`setup`, :meth:`draw`, and
    :meth:`finish` to customise strip appearance.
    """

    def setup(self, layout: Any) -> None:
        """
        Prepare the strip for drawing.

        Parameters
        ----------
        layout : object
            The facet layout information.
        """

    def draw(self, label_info: Any) -> Any:
        """
        Draw the strip label.

        Parameters
        ----------
        label_info : object
            Information about the label to draw.

        Returns
        -------
        object
            The drawn strip element.
        """

    def finish(self) -> None:
        """
        Finalise strip rendering.
        """
