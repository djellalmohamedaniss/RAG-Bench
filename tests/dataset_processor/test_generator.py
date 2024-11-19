import os

from dotenv import load_dotenv

from dataset_processor.generation import RAGGeneratorOpenAI

load_dotenv("../.env")


def test_rag_generation_openai():
    context = """
        Ces premiers ouvrages donnèrent naissance à des compilations, à des
        abrégés plus ou moins médiocres qui n'apprenoient rien de nouveau. Une
        dispute qui s'éleva quelques années après, entre deux savants[3], sur
        nos anciennes églises, sans éclaircir beaucoup la question qu'ils
        traitoient, répandit quelques nouvelles lumières sur les antiquités de
        Paris. Pendant ce temps, Henri Sauval, avocat au parlement,
        travailloit à nous donner des connoissances plus exactes et plus
        étendues sur un sujet aussi important. Il recueillit, dans les dépôts
        publics et dans les archives particulières, une quantité prodigieuse
        de documents et de titres sur l'état ancien et moderne de la ville de
        Paris, les lut, les dépouilla avec une patience infatigable; mais
        n'eut ni le temps ni peut-être le talent de les mettre en ordre, de
        les comparer, de les vérifier. Il en est résulté que son immense
        recueil n'est qu'un amas informe de matériaux confondus ensemble, et
        dont il est impossible d'user sans y apporter les plus grandes
        précautions. Il est plein de répétitions, de détails fatigants, de
        trivialités, inexact dans les faits, peu judicieux dans les
        réflexions; et ses erreurs sur une foule de matières, principalement
        sur l'appréciation des monuments, sont telles, qu'elles seroient
        insupportables aujourd'hui aux personnes même les moins éclairées.
        """
    num_generations = 3
    generator = RAGGeneratorOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    questions = generator.generate_questions(context, num_generations)
    assert len(questions["questions"]) == num_generations
    question = questions["questions"][0]
    answer = generator.generate_answers(context, [question])
    assert type(answer) is list
