from bokeh.models.layouts import Panel, Tabs
from bokeh.plotting import figure
from bokeh.models import (
    ColumnDataSource,
    HoverTool,
    Select,
    ColorPicker,
)
from bokeh.layouts import column, row


def covid(df):
    # Membuat data source
    def create_dataset(df):
        return ColumnDataSource(data=df)

    # Membuat line plot untuk kasus harian
    def daily_plot(src):
        # Membuat model plot
        p = figure(
            plot_width=1200,
            plot_height=700,
            x_axis_type="datetime",
            title="Kasus COVID-19 Harian",
            x_axis_label="Tanggal",
            y_axis_label="Kasus baru",
        )

        # Membuat line plot
        pm_line = p.line(
            source=src,
            x="date",
            y="daily_new_cases",
            line_width=2.3,
            color="lightskyblue",
            name="pm_line",
        )

        # Menambahkan hover
        hover = HoverTool(
            tooltips=[
                ("Tanggal", "@date{%F}"),
                ("Kasus baru", "@daily_new_cases"),
                ("Total kasus", "@cumulative_total_cases"),
            ],
            formatters={"@date": "datetime"},
            mode="vline",
        )

        p.add_tools(hover)

        # Menambahkan style plot
        p.title.align = "center"
        p.title.text_font_size = "16pt"

        return p

    # Membuat line plot untuk kasus kematian
    def death_plot(src):
        # Membuat model plot
        p = figure(
            plot_width=1200,
            plot_height=700,
            x_axis_type="datetime",
            title="Kematian COVID-19 Harian",
            x_axis_label="Tanggal",
            y_axis_label="Kematian baru",
        )

        # Membuat line plot
        pm_line = p.line(
            source=src,
            x="date",
            y="daily_new_deaths",
            line_width=2.3,
            color="lightskyblue",
            name="pm_line",
        )

        # Menambahkan hover
        hover = HoverTool(
            tooltips=[
                ("Tanggal", "@date{%F}"),
                ("Meninggal", "@daily_new_deaths"),
                ("Total meninggal", "@cumulative_total_deaths"),
            ],
            formatters={"@date": "datetime"},
            mode="vline",
        )

        p.add_tools(hover)

        # Menambahkan style plot
        p.title.align = "center"
        p.title.text_font_size = "16pt"

        return p

    # Membuat callback function untuk update plot
    def update_plot(attr, old, new):
        country = select.value
        new_df = df[df["country"] == country]
        new_src = create_dataset(new_df)
        src.data.update(new_src.data)

    # Init plot
    src = create_dataset(df[df["country"] == "Indonesia"])
    p_daily = daily_plot(src)
    p_death = death_plot(src)

    # Menambahkan dropdown select
    select = Select(
        options=list(df["country"].unique()), value="Indonesia", title="Country"
    )
    select.on_change("value", update_plot)

    # Menambahkan color picker
    pm_line = p_daily.select_one({"name": "pm_line"})
    pm_line2 = p_death.select_one({"name": "pm_line"})
    picker = ColorPicker(title="Line Color", color="lightskyblue")
    picker.js_link("color", pm_line.glyph, "line_color")
    picker.js_link("color", pm_line2.glyph, "line_color")

    # Set Layout
    controller1 = column(picker, select)
    controller2 = column(picker, select)
    layout = row([p_daily, controller1])
    layout2 = row([p_death, controller2])

    # Menambahkan tab
    tab1 = Panel(child=layout, title="Kasus Harian")
    tab2 = Panel(child=layout2, title="Kematian")

    tab = Tabs(tabs=[tab1, tab2])

    return tab
