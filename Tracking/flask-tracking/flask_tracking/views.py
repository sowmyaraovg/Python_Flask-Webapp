from flask import Blueprint, flash, Markup, redirect, render_template, url_for

from .forms import SectionForm,SectionContentForm,DocsForm,GapsForm
from .models import db, query_to_list, Section, SectionContent,Docs,Gaps


tracking = Blueprint("tracking", __name__)


@tracking.route("/")
def index():
    section_form = SectionForm()
    sc_form = SectionContentForm()
    doc_form=DocsForm()
    gap_form=GapsForm()
    return render_template("index.html",
                           section_form=section_form,
                           sc_form=sc_form,
                           doc_form=doc_form,
                           gap_form=gap_form)


@tracking.route("/section", methods=("POST", ))
def add_site():
    form = SectionForm()
    if form.validate_on_submit():
        section = Section()
        form.populate_obj(section)
        db.session.add(section)
        db.session.commit()
        #flash("Added site")
        return redirect(url_for(".index"))

    return render_template("validation_error.html", form=form)


@tracking.route("/section/<int:section_id>")
def view_site_visits(section_id=None):
    section = Section.query.get_or_404(section_id)
    query = SectionContent.query.filter(SectionContent.section_id == section_id)
    data = query_to_list(query)
    title = "visits for {}".format(section.SectionTitle)
    return render_template("data_list.html", data=data, title=title)


@tracking.route("/sectioncontent", methods=("POST", ))
@tracking.route("/section/<int:section_id>/sectioncontent", methods=("POST",))
def add_visit(section_id=None):
    if section_id is None:
        # This is only used by the visit_form on the index page.
        form = SectionContentForm()
    else:
        section = Section.query.get_or_404(section_id)
        # WTForms does not coerce obj or keyword arguments
        # (otherwise, we could just pass in `site=site_id`)
        # CSRF is disabled in this case because we will *want*
        # users to be able to hit the /site/:id endpoint from other sites.
        form = SectionContentForm(csrf_enabled=False, section=section)

    if form.validate_on_submit():
        sectioncontent= SectionContent()
        scenarioname=sectioncontent.ScenarioName
        #form.populate_obj(sectioncontent)
        form.populate_obj(scenarioname)

        sectioncontent.section_id = form.section.data.id
        db.session.add(scenarioname)
        db.session.commit()
        #flash("Added visit for site {}".format(form.section.data.SectionTitle))
        return redirect(url_for(".index"))

    return render_template("validation_error.html", form=form)

@tracking.route("/sections")
def view_sites():
    query = Section.query.filter(Section.id >= 0)
    data = query_to_list(query)

    # The header row should not be linked
    results = [next(data)]
    for row in data:
        row = [_make_link(cell) if i == 0 else cell
               for i, cell in enumerate(row)]
        results.append(row)

    return render_template("data_list.html", data=results, title="Sections")


_LINK = Markup('<a href="{url}">{name}</a>')


def _make_link(section_id):
    url = url_for(".view_site_visits", section_id=section_id)
    return _LINK.format(url=url, name=section_id)

