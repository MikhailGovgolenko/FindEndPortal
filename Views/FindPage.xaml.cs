using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Controls;
using Microsoft.UI.Xaml.Controls.Primitives;
using Microsoft.UI.Xaml.Data;
using Microsoft.UI.Xaml.Input;
using Microsoft.UI.Xaml.Media;
using Microsoft.UI.Xaml.Navigation;
using Microsoft.Windows.ApplicationModel.Resources;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Runtime.InteropServices.WindowsRuntime;
using Windows.ApplicationModel.DataTransfer;
using Windows.ApplicationModel.Resources;
using Windows.Foundation;
using Windows.Foundation.Collections;
using System.Text.RegularExpressions;
using Microsoft.UI;
using static PInvoke.User32;
using Microsoft.UI.Xaml.Documents;
using Microsoft.UI.Xaml.Shapes;

// To learn more about WinUI, the WinUI project structure,
// and more about our project templates, see: http://aka.ms/winui-project-info.

namespace FindEndPortal.Views;


/// <summary>
/// An empty page that can be used on its own or navigated to within a Frame.
/// </summary>
public sealed partial class FindPage : Page
{
    public FindPage()
    {
        this.InitializeComponent();
        this.Loaded += MainPage_Loaded;
    }

    readonly string CoordinatePattern = @"(^[+-]?0*[0-9]{1,7}(\.[0-9]*)?|\.[0-9]+$)|
                                (^[+-]?0*1[0-9]{7}(\.[0-9]*)?$)|
                                (^[+-]?0*2[0-8][0-9]{6}(\.[0-9]*)?$)|
                                (^[+-]?0*29[0-8][0-9]{5}(\.[0-9]*)?$)|
                                (^[+-]?0*299[0-8][0-9]{4}(\.[0-9]*)?$)|
                                (^[+-]?0*2999[0-8][0-9]{3}(\.[0-9]*)?$)|
                                (^[+-]?0*29999[0-8][0-9]{2}(\.[0-9]*)?$)|
                                (^[+-]?0*299999[0-7][0-9](\.[0-9]*)?$)|
                                (^\-0*2999998[0-3](\.[0-9]*)?$)|
                                (^[+]?0*2999998[0-2](\.[0-9]*)?$)|
                                (^\-0*29999984(\.[0]*)?$)|
                                (^[+]?0*29999983(\.[0]*)?$)";
    readonly string AnglePattern = @"[+-]?([0-9]+([.][0-9]*)?|[.][0-9]+)";

    private bool ValidateString(string input, string pattern)
    {
        var match = Regex.Match(input, pattern);
        return match.Success && match.Value.Length == input.Length;
    }

    private void MainPage_Loaded(object sender, RoutedEventArgs e)
    {
        RefreshUIText();
    }

    private void RefreshUIText()
    {
        var resourceLoader = Windows.ApplicationModel.Resources.ResourceLoader.GetForViewIndependentUse();
        this.angle1.PlaceholderText = resourceLoader.GetString("Angle/Text");
        this.angle2.PlaceholderText = resourceLoader.GetString("Angle/Text");
    }

    private void Clear(object sender, RoutedEventArgs e)
    {
        x1.Text = "";
        z1.Text = "";
        angle1.Text = "";
        x2.Text = "";
        z2.Text = "";
        angle2.Text = "";
        x0.Text = "";
        z0.Text = "";
    }

    private void CopyText_Click(object sender, RoutedEventArgs args)
    {
        if (x0.Text != "" & z0.Text != "")
        {
            var package = new DataPackage();
            package.SetText("tp @s " + x0.Text + " ~ " + z0.Text);
            Clipboard.SetContent(package);
        }
    }

    private async void PasteText_Click1(object sender, RoutedEventArgs args)
    {
        var package = Clipboard.GetContent();
        if (package.Contains(StandardDataFormats.Text))
        {
            var text = await package.GetTextAsync();
            var text_mass = text.Split(" ");
            x1.Text = text_mass[6];
            z1.Text = text_mass[8];
            angle1.Text = Convert.ToString(Math.Round(Math.Round(Convert.ToDouble(text_mass[9].Replace('.', ',')), 2) % 360, 2)).Replace(',', '.');
            if (!(ValidateString(x1.Text, CoordinatePattern) && 
                  ValidateString(z1.Text, CoordinatePattern) && 
                  ValidateString(angle1.Text, CoordinatePattern)))
            {
                x1.Text = "";
                z1.Text = "";
                angle1.Text = "";
            }
        }
    }

    private async void PasteText_Click2(object sender, RoutedEventArgs args)
    {
        var package = Clipboard.GetContent();
        if (package.Contains(StandardDataFormats.Text))
        {
            var text = await package.GetTextAsync();
            var text_mass = text.Split(" ");
            x2.Text = text_mass[6];
            z2.Text = text_mass[8];
            angle2.Text = Convert.ToString(Math.Round(Math.Round(Convert.ToDouble(text_mass[9].Replace('.', ',')), 2) % 360, 2)).Replace(',', '.');
            if (!(ValidateString(x2.Text, CoordinatePattern) &&
                  ValidateString(z2.Text, CoordinatePattern) &&
                  ValidateString(angle2.Text, CoordinatePattern)))
            {
                x2.Text = "";
                z2.Text = "";
                angle2.Text = "";
            }
        }
    }

    static double Decart(double Angle)
    {
        return (Angle + 90);
    }

    static double Radians(double Angle)
    {
        return Angle * Math.PI / 180;
    }

    private static int PyInt(double x)
    {
        var a = Convert.ToDecimal(x);
        return Convert.ToInt32(Math.Floor(Math.Abs(a))) * Math.Sign(a);
    }

    private bool Condition(double Angle, double coordinate_x, double coordinate_z, double c_x, double c_z)
    {
        var sina = Math.Round(Math.Sin(Radians(Angle)), 10);
        var cosa = Math.Round(Math.Cos(Radians(Angle)), 10);
        var cond = true;

        if (0 <= cosa && cosa <= 1 && 0 <= sina && sina < 1)
        {
            cond = coordinate_x >= c_x;
        }

        if (-1 < cosa && cosa <= 0 && 0 <= sina && sina <= 1) 
        {
            cond = coordinate_z >= c_z;
        }

        if (-1 <= cosa && cosa <= 0 && -1 < sina && sina <= 0)
        {
            cond = coordinate_x <= c_x;
        }

        if (0 <= cosa && cosa < 1 && -1 <= sina && sina <= 0)
        {
            cond = coordinate_z <= c_z;
        }
        return cond;
    }

    private void Calculations(TextBox sender, TextBoxTextChangingEventArgs args)
    {
        TextBox[] lines = {x1, x2, z1, z2, angle1, angle2};
        var allValid = true;

        foreach (var line in lines)
        {
            if (line == x1 || line == x2 || line == z1 || line == z2)
            {
                if (!ValidateString(line.Text, CoordinatePattern))
                {
                    allValid = false;
                }
            }
            if ((line == angle1) || (line == angle2))
            {
                if (!ValidateString(line.Text, AnglePattern))
                {
                    allValid = false;
                }
            }
        }

        if (! allValid)
        {
            x0.Text = "";
            z0.Text = "";
        }

        else
        {
            var tx1 = Convert.ToDouble(x1.Text.Replace(".", ","));
            var tz1 = Convert.ToDouble(z1.Text.Replace(".", ","));
            var tx2 = Convert.ToDouble(x2.Text.Replace(".", ","));
            var tz2 = Convert.ToDouble(z2.Text.Replace(".", ","));
            var alpha = Convert.ToDouble(angle1.Text.Replace(".", ","));
            var beta = Convert.ToDouble(angle2.Text.Replace(".", ","));

            double x;
            double z;

            if (Decart(alpha) == Decart(beta))
            {
                var resourceLoader = Windows.ApplicationModel.Resources.ResourceLoader.GetForViewIndependentUse();
                x0.Text = resourceLoader.GetString("Error/Text");
                z0.Text = resourceLoader.GetString("Error_Parallel/Text");
            }
            else
            {
                x = (tz2 - tz1 + Math.Tan(Radians(Decart(alpha))) * tx1 - Math.Tan(Radians(Decart(beta))) * tx2) / (Math.Tan(Radians(Decart(alpha))) - Math.Tan(Radians(Decart(beta))));
                z = ((tx1 - tx2) * Math.Tan(Radians(Decart(alpha))) * Math.Tan(Radians(Decart(beta))) + Math.Tan(Radians(Decart(alpha))) * tz2 - Math.Tan(Radians(Decart(beta))) * tz1) / (Math.Tan(Radians(Decart(alpha))) - Math.Tan(Radians(Decart(beta))));

                if (!((-29999984 <= x && x <= 29999983) || (-29999984 <= z && z <= 29999983)))
                {
                    var resourceLoader = Windows.ApplicationModel.Resources.ResourceLoader.GetForViewIndependentUse();
                    x0.Text = resourceLoader.GetString("Error/Text");
                    z0.Text = resourceLoader.GetString("Error_Out/Text");
                }

                else if (Condition(Decart(alpha), x, z, tx1, tz1) && Condition(Decart(beta), x, z, tx2, tz2))
                {
                    x0.Text = PyInt(x).ToString();
                    z0.Text = PyInt(z).ToString();
                }
                else
                {
                    var resourceLoader = Windows.ApplicationModel.Resources.ResourceLoader.GetForViewIndependentUse();
                    x0.Text = resourceLoader.GetString("Error/Text");
                    z0.Text = resourceLoader.GetString("Error_Intersection/Text");
                }
            }
        }
    }
}