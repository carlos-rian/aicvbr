import json
from enum import Enum
from textwrap import dedent

from linkedin_api import Linkedin

from ..logger import Logger
from ..schema import BaseModel


class Period(BaseModel):
    year: int  # experience > timePeriod > * > year
    month: int = None  # experience > timePeriod > * > month


class TimePeriod(BaseModel):
    start_date: Period  # experience > timePeriod > startDate
    end_date: Period | None = None  # experience > timePeriod > endDate


class EmployeeCountRange(BaseModel):
    start: int  # experience > company > employeeCountRange > start
    end: int | None = None  # experience > company > employeeCountRange > end


class Company(BaseModel):
    employee_count_range: EmployeeCountRange  # experience > company > employeeCountRange
    industries: list[str]  # experience > company > industries


class Expirience(BaseModel):
    # job description
    title: str  # experience > title
    description: str | None = None  # experience > description
    company_name: str  # experience > companyName
    location_name: str | None = None  # experience > locationName
    company: Company | None = None  # experience > company


class Education(BaseModel):
    degree_name: str | None = None  # education > degreeName
    field_of_study: str  # education > fieldOfStudy
    school_name: str  # education > schoolName
    time_period: TimePeriod  # education > timePeriod


class Certification(BaseModel):
    authority: str  # certifications > authority
    name: str  # certifications > name
    time_period: TimePeriod


class EnumProficiency(str, Enum):
    ELEMENTARY = "ELEMENTARY"  # (Elementary proficiency)
    LIMITED_WORKING = "LIMITED_WORKING"  # (Limited working proficiency)
    PROFESSIONAL_WORKING = "PROFESSIONAL_WORKING"  # (Professional working proficiency)
    FULL_PROFESSIONAL = "FULL_PROFESSIONAL"  # (Full professional proficiency)
    NATIVE_OR_BILINGUAL = "NATIVE_OR_BILINGUAL"  # (Native or bilingual proficiency)


class Language(BaseModel):
    name: str  # name
    proficiency: EnumProficiency  # proficiency


class Skill(BaseModel):
    name: str  # name


class Profile(BaseModel):
    urn_id: str  # urn_id
    first_name: str  # firstName
    last_name: str  # lastName
    public_id: str  # public_id
    summary: str | None = None  # summary
    industry_name: str | None = None  # industryName
    headline: str | None = None  # headline
    # location
    geo_country_name: str  # locationName
    geo_location_name: str  # geoLocationName
    # experiences
    experience: list[Expirience] | None = None  # experiences > experience
    # educations
    education: list[Education] | None = None  # educations > education
    # languages
    languages: list[Language] | None = None  # languages > language
    # certifications
    certifications: list[Certification] | None = None  # certifications > certification
    # skills
    skills: list[Skill] | None = None  # skills > skill


class LinkedinCrawler:
    def __init__(self, username: str, password: str):
        self.api = Linkedin(username=username, password=password)
        self.profile = None

    def get_profile_skills(self, urn_id: str) -> list:
        skills = self.api.get_profile_skills(urn_id=urn_id)
        if not skills:
            return []

        return [Skill.model_validate(skill) for skill in skills]

    def get_profile(self, public_id: str) -> Profile | None:
        profile = self.api.get_profile(public_id)
        if not profile:
            return None
        Logger.info(f"Profile found: {json.dumps(profile, indent=2)}")
        profile = Profile.model_validate(profile)
        profile.skills = self.get_profile_skills(urn_id=profile.urn_id)
        self.profile = profile
        return profile

    def _format_experience(self) -> Expirience:
        if not self.profile.experience:
            return "Not informed"

        def get_employee_count_range(company: Company | None) -> str:
            if not company:
                return "Not informed"

            return f"{company.employee_count_range.start} - {company.employee_count_range.end or '-'}"

        text = ""
        for idx, experience in enumerate(self.profile.experience):
            text += dedent(f"""
Experience {idx}:
 - Title: {experience.title}
 - Company Name: {experience.company_name}
 - Location Name: {experience.location_name or "Not informed"}
 - Employee Count Range: {get_employee_count_range(experience.company)}
 - Industries: {', '.join(experience.company.industries) if experience.company else "Not informed"}
 - Description: {experience.description or "Not informed"}
\n""")

        return dedent(text)

    def _format_education(self) -> str:
        if not self.profile.education:
            return "Not informed"

        text = ""

        for idx, education in enumerate(self.profile.education):
            end_date = "Not informed"
            if education.time_period.end_date:
                end_date = f"{education.time_period.end_date.year}/{education.time_period.end_date.month or '-'}"

            text += dedent(f"""
Education {idx}:
 - Degree Name: {education.degree_name or "Not informed"}
 - Field of Study: {education.field_of_study}
 - School Name: {education.school_name}
 - Start Date: {education.time_period.start_date.year}/{education.time_period.start_date.month or '-'}
 - End Date: {end_date}
\n""")

        return dedent(text)

    def _format_certifications(self) -> str:
        if not self.profile.certifications:
            return "Not informed"

        text = ""

        for idx, certification in enumerate(self.profile.certifications):
            end_date = "Not informed"
            if certification.time_period.end_date:
                end_date = (
                    f"{certification.time_period.end_date.year}/{certification.time_period.end_date.month or '-'}"
                )

            text += dedent(f"""
Certification {idx}:
 - Authority: {certification.authority}
 - Name: {certification.name}
 - Start Date: {certification.time_period.start_date.year}/{certification.time_period.start_date.month or '-'}
 - End Date: {end_date}
\n""")

        return dedent(text)

    def _format_languages(self) -> str:
        text = ""

        for idx, language in enumerate(self.profile.languages):
            text += dedent(f"""
Language {idx}:
 - Name: {language.name}
 - Proficiency: {language.proficiency}
\n""")

        return dedent(text)

    def _format_skills(self) -> str:
        return ", ".join([skill.name for skill in self.profile.skills])

    def format_as_text(self):
        return dedent(f"""
Profile:
 - Headline: {self.profile.headline}
 - Summary: {self.profile.summary}
 - Location: {self.profile.geo_country_name} - {self.profile.geo_location_name}
 - Industry: {self.profile.industry_name}

Experiences:
{self._format_experience()}

Educations:
{self._format_education()}

Certifications:
{self._format_certifications()}

Languages:
{self._format_languages()}

Skills: {self._format_skills()}
""")
