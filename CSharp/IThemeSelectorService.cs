using Microsoft.UI.Xaml;

namespace FindEndPortal;

public interface IThemeSelectorService
{
    ElementTheme GetTheme();
    void SetTheme(ElementTheme theme);
}
