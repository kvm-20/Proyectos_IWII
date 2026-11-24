"""Datos iniciales del catalogo: obras de dominio público con un fragmento de muestra.

Cada párrafo separado por una linea en blanco es una 'página' en el visor de lectura.
"""

NOTA_FINAL = (
    "Fin del fragmento de muestra. Esta obra es de dominio público: puedes leerla completa "
    "en Project Gutenberg con el boton 'Obra completa'."
)

LIBROS = [
    {
        "titulo": "María",
        "autor": "Jorge Isaacs",
        "categoria": "Novela",
        "anio": 1867,
        "idioma": "Español",
        "descripcion": "Novela romántica colombiana ambientada en el Valle del Cauca. "
        "Efraín regresa a la hacienda familiar y se enamora de su prima María.",
        "url_externa": "https://www.gutenberg.org/ebooks/search/?query=Maria+Jorge+Isaacs",
        "contenido": (
            "Era yo niño aún cuando me alejaron de la casa paterna para que diera principio a mis "
            "estudios en el colegio del doctor Lorenzo María Lleras, establecido en Bogotá hacía "
            "pocos años, y famoso en toda la República por aquel tiempo.\n\n"
            "En la noche víspera de mi viaje, después de la velada, entró a mi cuarto una de mis "
            "hermanas, y sin decirme una sola palabra cariñosa, porque los sollozos le embargaban "
            "la voz, cortó de mi cabeza unos cabellos: cuando salió, habían rodado por mi cuello "
            "algunas lágrimas suyas.\n\n" + NOTA_FINAL
        ),
    },
    {
        "titulo": "Don Quijote de la Mancha",
        "autor": "Miguel de Cervantes",
        "categoria": "Clásicos",
        "anio": 1605,
        "idioma": "Español",
        "descripcion": "Un hidalgo enloquece leyendo libros de caballerías y sale a recorrer "
        "España como caballero andante junto a su escudero Sancho Panza.",
        "url_externa": "https://www.gutenberg.org/ebooks/2000",
        "contenido": (
            "En un lugar de la Mancha, de cuyo nombre no quiero acordarme, no ha mucho tiempo que "
            "vivía un hidalgo de los de lanza en astillero, adarga antigua, rocín flaco y galgo "
            "corredor.\n\n"
            "Una olla de algo más vaca que carnero, salpicón las más noches, duelos y quebrantos "
            "los sábados, lantejas los viernes, algún palomino de añadidura los domingos, "
            "consumían las tres partes de su hacienda.\n\n"
            "Frisaba la edad de nuestro hidalgo con los cincuenta años; era de complexión recia, "
            "seco de carnes, enjuto de rostro, gran madrugador y amigo de la caza.\n\n" + NOTA_FINAL
        ),
    },
    {
        "titulo": "Lazarillo de Tormes",
        "autor": "Anónimo",
        "categoria": "Clásicos",
        "anio": 1554,
        "idioma": "Español",
        "descripcion": "Novela picaresca en la que Lázaro cuenta su vida al servicio de varios amos.",
        "url_externa": "https://www.gutenberg.org/ebooks/search/?query=Lazarillo+de+Tormes",
        "contenido": (
            "Pues sepa Vuestra Merced, ante todas cosas, que a mí llaman Lázaro de Tormes, hijo de "
            "Tomé González y de Antona Pérez, naturales de Tejares, aldea de Salamanca.\n\n"
            + NOTA_FINAL
        ),
    },
    {
        "titulo": "Pride and Prejudice",
        "autor": "Jane Austen",
        "categoria": "Novela",
        "anio": 1813,
        "idioma": "Inglés",
        "descripcion": "Elizabeth Bennet y el señor Darcy superan el orgullo y los prejuicios "
        "en la Inglaterra rural del siglo XIX.",
        "url_externa": "https://www.gutenberg.org/ebooks/1342",
        "contenido": (
            "It is a truth universally acknowledged, that a single man in possession of a good "
            "fortune, must be in want of a wife.\n\n"
            "However little known the feelings or views of such a man may be on his first entering "
            "a neighbourhood, this truth is so well fixed in the minds of the surrounding families, "
            "that he is considered the rightful property of some one or other of their daughters.\n\n"
            "\"My dear Mr. Bennet,\" said his lady to him one day, \"have you heard that Netherfield "
            "Park is let at last?\"\n\n" + NOTA_FINAL
        ),
    },
    {
        "titulo": "Alice's Adventures in Wonderland",
        "autor": "Lewis Carroll",
        "categoria": "Fantasía",
        "anio": 1865,
        "idioma": "Inglés",
        "descripcion": "Alicia persigue a un conejo blanco y cae en un mundo absurdo y fantástico.",
        "url_externa": "https://www.gutenberg.org/ebooks/11",
        "contenido": (
            "Alice was beginning to get very tired of sitting by her sister on the bank, and of "
            "having nothing to do: once or twice she had peeped into the book her sister was "
            "reading, but it had no pictures or conversations in it, \"and what is the use of a "
            "book,\" thought Alice \"without pictures or conversations?\"\n\n"
            "So she was considering in her own mind (as well as she could, for the hot day made "
            "her feel very sleepy and stupid), whether the pleasure of making a daisy-chain would "
            "be worth the trouble of getting up and picking the daisies, when suddenly a White "
            "Rabbit with pink eyes ran close by her.\n\n" + NOTA_FINAL
        ),
    },
    {
        "titulo": "Frankenstein",
        "autor": "Mary Shelley",
        "categoria": "Ciencia ficción",
        "anio": 1818,
        "idioma": "Inglés",
        "descripcion": "Víctor Frankenstein da vida a una criatura y debe enfrentar las "
        "consecuencias de su creación.",
        "url_externa": "https://www.gutenberg.org/ebooks/84",
        "contenido": (
            "You will rejoice to hear that no disaster has accompanied the commencement of an "
            "enterprise which you have regarded with such evil forebodings.\n\n"
            "I arrived here yesterday, and my first task is to assure my dear sister of my welfare "
            "and increasing confidence in the success of my undertaking.\n\n" + NOTA_FINAL
        ),
    },
    {
        "titulo": "The Adventures of Sherlock Holmes",
        "autor": "Arthur Conan Doyle",
        "categoria": "Misterio",
        "anio": 1892,
        "idioma": "Inglés",
        "descripcion": "Doce casos del detective Sherlock Holmes narrados por el doctor Watson.",
        "url_externa": "https://www.gutenberg.org/ebooks/1661",
        "contenido": (
            "To Sherlock Holmes she is always the woman. I have seldom heard him mention her under "
            "any other name.\n\n"
            "In his eyes she eclipses and predominates the whole of her sex.\n\n" + NOTA_FINAL
        ),
    },
]

RESENAS_DEMO = [
    # (titulo del libro, calificacion, comentario)
    ("María", 5, "Un clásico colombiano, la descripción del Valle es hermosa."),
    ("Don Quijote de la Mancha", 4, "Largo pero muy divertido."),
    ("Alice's Adventures in Wonderland", 5, "Perfecto para practicar inglés."),
]
