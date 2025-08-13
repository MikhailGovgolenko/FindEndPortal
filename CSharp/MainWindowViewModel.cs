using System.Windows.Input;
using CommunityToolkit.Mvvm.Input;
using System;
using CommunityToolkit.Mvvm.ComponentModel;
using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Media;
using Microsoft.UI;

namespace FindEndPortal;

public class MainWindowViewModel : ObservableObject
{
    private string? _topTitle;
    private SolidColorBrush? _themeColor;
    private string? _textBoxText;
    private readonly IThemeSelectorService _themeSelectorService;


    public string? TopTitle
    {
        get => _topTitle;
        set => SetProperty(ref _topTitle, value);
    }

    public SolidColorBrush? ThemeColor
    {
        get => _themeColor;
        set => SetProperty(ref _themeColor, value);
    }

    public string? TextBoxText
    {
        get => _textBoxText;
        set => SetProperty(ref _textBoxText, value);
    }

    public ICommand SetThemeCommand { get; }

    public MainWindowViewModel(IThemeSelectorService themeSelectorService)
    {
        SetThemeCommand = new RelayCommand<string>((theme) => UpdateTheme(theme));
        _themeSelectorService = themeSelectorService;
    }

    private void UpdateTheme(string themeName)
    {
        if (Enum.TryParse(themeName, out ElementTheme theme) is true)
        {
            _themeSelectorService.SetTheme(theme);
        }
    }
}
