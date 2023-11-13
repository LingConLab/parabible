default_lang ='ru'

language_format_options = {
    'lang_name': {
        'en': 'Language name',
        'ru': 'Название языка'
    },
    'closest_iso_639_3': {
        'en': 'Closest ISO 639-3',
        'ru': 'Ближайший ISO 639-3'
    },
    'iso_15924': {
        'en': 'ISO 15924',
        'ru': 'ISO 15924'
    },
}

translations_base = {
    "nav_name": {
        "en": "Parabible",
        "ru": "Parabible"
    },
    "nav_search": {
        "en": "Search",
        "ru": "Поиск"
    },
    "nav_how_to_use": {
        "en": "How to use",
        "ru": "Как пользоваться"
    },
    "nav_lang": {
        "en": "English",
        "ru": "Russian"
    }
}

translations_home = {
    "about_label": {
        "en": "About the corpus",
        "ru": "О корпусе"
    },
    "about_text": {
        "en": "Parabible is a parallel corpus containing 1800+ bible translations. Right now it is in early development stage.",
        "ru": "Парабиблия это параллельный корпус содержащий более 1800 переводов библии. В данный момент корпус находится в стадии ранней разработки."
    },
}

translations_search = {
    "choose_translations_label": {
        "en": "Choose translations",
        "ru": "Выбор переводов"
    },
    "choose_translations_hint": {
        "en": "'Add translation'  button may be pressed only after translation is selected.",
        "ru": "Кнопка 'Добавить перевод' может быть нажата только после выбора перевода"
    },
    "choose_verses_label": {
        "en": "Choose verses",
        "ru": "Выбор стихов"
    },
    "choose_verses_hint": {
        "en": "This block will be active only after at least one translation is added. 'Add verse' may be pressed only after verse number is selected.",
        "ru": "Этот блок будет доступен только после добавления хотя бы одного перевода. 'Добавить стих' может быть нажата только после выбора номера стиха."
    },
    "raw_request_label": {
        "en": "Raw request",
        "ru": "Запрос"
    },
    "raw_request_hint": {
        "en": "This field exists so you can save your request configuration (chosen verses and translations). Copy the text from this field and save it somewhere. Then paste it here when you need it again. And don't forget to press the 'Submit' button.",
        "ru": "Это поле существует для того, чтобы вы могли сохранять свои настройки выдачи (список добавленных стихов и переводов). Скопируйте текст этого поля и сохраните себе куда-нибудь, а потом вставьте его когда вам понадобится этот набор стихов в следующий раз. Не забудьте нажать кнопку 'Отправить запрос'."
    },
    "language_format_label": {
        "en": "Language format",
        "ru": "Формат языка"
    },
    "language_label": {
        "en": "Language",
        "ru": "Язык"
    },
    "translation_label": {
        "en": "Translation",
        "ru": "Перевод"
    },
    "add_translation_button_text": {
        "en": "Add translation",
        "ru": "Добавить перевод"
    },
    "book_label": {
        "en": "Book",
        "ru": "Книга"
    },
    "chapter_label": {
        "en": "Chapter",
        "ru": "Глава"
    },
    "verse_label": {
        "en": "Verse",
        "ru": "Стих"
    },
    "add_verse_button_text": {
        "en": "Add verse",
        "ru": "Добавить стих"
    },
    "verse_filter_mode_label": {
        "en": "Show options that are translated in",
        "ru": "Показывать опции, которые переведены"
    },
    "verse_filter_mode_all_label": {
        "en": "ALL selected translations ",
        "ru": "во ВСЕХ выбранных переводах сразу"
    },
    "verse_filter_mode_any_label": {
        "en": "at least ONE selected translation",
        "ru": "хотя бы в ОДНОМ выбранном переводе"
    },
    "raw_request_button_text": {
        "en": "Submit",
        "ru": "Отправить запрос"
    }
}

translations_how_to_use = {
    "h_1": {
        "en": "How to use",
        "ru": "Как пользоваться"
    },
    "p_1_1": {
        "en": "You can search in corpus on",
        "ru": "Поиск осуществляется на"
    },
    "a_search_page": {
        "en": "this page",
        "ru": "этой странице"
    },
    "p_1_2": {
        "en": f"(the button \"{translations_base['nav_search']['en']}\" on the top panel). You can see three blocks on the search page: " + \
              f"\"{translations_search['choose_translations_label']['en']}\", \"{translations_search['choose_verses_label']['en']}\" and \"{translations_search['raw_request_label']['en']}\". " + \
              "Follow these steps to get your search results: ",
        "ru": f"(кнопка \"{translations_base['nav_search']['ru']}\" на верхней палени). На странице поиска вы увидите три блока: " + \
              f"\"{translations_search['choose_translations_label']['ru']}\", \"{translations_search['choose_verses_label']['ru']}\" и \"{translations_search['raw_request_label']['ru']}\". " + \
              "Для получения выдачи вам необходимо последовательно: "
    },
    "li_translation_adding_1": {
        "en": f"Add at least one translation using \"{translations_search['choose_translations_label']['en']}\" block:",
        "ru": f"Добавить хотя бы один перевод в блоке \"{translations_search['choose_translations_label']['ru']}\":"
    },
    "li_translation_adding_subitem_1": {
        "en": f"Choose a language format in \"{translations_search['language_format_label']['en']}\" dropdown list",
        "ru": f"Выберите в каком формате вы хотите выбирать язык в выпадающем списке \"{translations_search['language_format_label']['ru']}\""
    },
    "li_translation_adding_subitem_2": {
        "en": f"Choose a language in \"{translations_search['language_label']['en']}\" dropdown list",
        "ru": f"Выберите язык в выбранном вами формате в выпадающем списке \"{translations_search['language_label']['ru']}\""
    },
    "li_translation_adding_subitem_3": {
        "en": f"Choose a translation in \"{translations_search['translation_label']['en']}\" dropdown list",
        "ru": f"Выберите перевод в выпадающем списке \"{translations_search['translation_label']['ru']}\""
    },
    "li_translation_adding_subitem_4": {
        "en": f"Add a chosen translation by clicking \"{translations_search['add_translation_button_text']['en']}\" button",
        "ru": f"Добавьте выбранный перевод, нажав кнопку \"{translations_search['add_translation_button_text']['ru']}\""
    },
    "li_translation_adding_2": {
        "en": "After completing these steps you will see a box with your chosen translation under the " + \
              f" \"{translations_search['add_translation_button_text']['en']}\" button. " + \
              "You can delete a translation by pressing a red cross button. You will also see, " + \
              f"that the first element of \"{translations_search['choose_verses_label']['en']}\" block turned active.",
        "ru": f"После выполнения этих шагов вы должны увидеть, что снизу от кнопки \"{translations_search['add_translation_button_text']['ru']}\" " + \
              "появилась коробочка с названием вашего перевода. Удалить его можно нажатием на красный крестик коробочки. Также вы увидите, " + \
              f"что первый элемент блока \"{translations_search['choose_verses_label']['ru']}\" стал активным."
    },
    "li_verse_adding_1": {
        "en": f"Add at least one verse using \"{translations_search['choose_verses_label']['en']}\" block:",
        "ru": f"Добавить хотя бы один стих в блоке \"{translations_search['choose_verses_label']['ru']}\":"
    },
    "li_verse_adding_subitem_1": {
        "en": f"Choose a book in \"{translations_search['book_label']['en']}\" dropdown list",
        "ru": f"Выберите книгу в выпадающем списке \"{translations_search['book_label']['ru']}\""
    },
    "li_verse_adding_subitem_2": {
        "en": f"Choose a chapter in \"{translations_search['chapter_label']['en']}\" dropdown list",
        "ru": f"Выберите главу в выпадающем списке \"{translations_search['chapter_label']['ru']}\""
    },
    "li_verse_adding_subitem_3": {
        "en": f"Choose a verse in \"{translations_search['verse_label']['en']}\" dropdown list",
        "ru": f"Выберите стих в выпадающем списке \"{translations_search['verse_label']['ru']}\""
    },
    "li_verse_adding_subitem_4": {
        "en": f"Add a chosen verse by clicking \"{translations_search['add_verse_button_text']['en']}\" button",
        "ru": f"Добавьте выбранный стих, нажав кнопку \"{translations_search['add_verse_button_text']['ru']}\""
    },
    "li_verse_adding_2": {
        "en": f"You will see a box with selected verse appear under \"{translations_search['add_verse_button_text']['ru']}\" " + \
              "button. arAfter completing said steps you can get your results by clicking " + \
              f"\"{translations_search['raw_request_button_text']['en']}\" button, " + \
              f"which is located at the bottom of \"{translations_search['raw_request_label']['en']}\" block.",
        "ru": f"Ваш выбранный стих должен также появиться в коробочке снизу от кнопки \"{translations_search['add_verse_button_text']['ru']}\"." + \
              "После выполнения этих шагов вы можете получить свою выдачу, нажав кнопку " + \
              f"\"{translations_search['raw_request_button_text']['ru']}\", " + \
              f"которая находится внизу блока \"{translations_search['raw_request_label']['ru']}\"."
    },
    "li_verse_adding_3": {
        "en": "Note: while chosing verses you will be given only those options (books, chapters, verses), that " + \
              f"are present in translations that you added. You can also define how these options are selected " + \
              f"with a switch that is located at the bottom of \"{translations_search['choose_verses_label']['en']}\" " + \
              "block. This switch has two states: either show options that are present in EVERY added translation, " + \
              "or show options that are present in AT LEAST ONE added translation.",
        "ru": "Примечание: во время выбора стихов вам будут предлагаться только те опции (книги, главы, стихи), которые " + \
              f"присутствуют в добавленных вами переводах. Внизу блока \"{translations_search['choose_verses_label']['ru']}\" " + \
              "есть переключатель, который позволит вам выбрать принцип подбора предложенных вариантов: или показывать " + \
              "варианты, которые есть ОДНОВРЕМЕННО ВО ВСЕХ добавленных вами переводах или показывать варианты, которые " + \
              "есть ХОТЯ БЫ В ОДНОМ из добавленных вами переводах."
    },
    "li_raw_box": {
        "en": f"\"{translations_search['raw_request_label']['en']}\" block:",
        "ru": f"Блок \"{translations_search['raw_request_label']['ru']}\":"
    },
    "p_raw_box_1": {
        "en": f"You might have already noticed, that the text is changing inside of \"{translations_search['raw_request_label']['en']}\"'s " + \
              "textbox every time you add or remove a translation or verse. This text unambiguously represents your query, " + \
              "it contains a list of added verses and a list of translation ids.",
        "ru": f"Вы могли заметить, что в текстовом поле внутри блока \"{translations_search['raw_request_label']['ru']}\" " + \
              "появлялся и менялся текст каждый раз, когда вы добавляли или удаляли стих или перевод. Текст в этом " + \
              "текстовом поле однозначно представляет ваш запрос, он содержит список стихов и список идентификаторов переводов. "
    },
    "p_raw_box_2": {
        "en": "In case you have a verses and translations combination that you will reuse upon your next visits, " + \
              f"you can save somewhere for yourself the text from this textbox, paste it there next time and click \"{translations_search['raw_request_button_text']['en']}\" " + \
              "button. This way you can avoid the process of adding every single translation and verse by hand every time.",
        "ru": "Если у вас есть какая-либо комбинация переводов и стихов, которую вы будете повторно запрашивать при " + \
              "последующих посещениях сайта, то вы можете скопировать и сохранить себе куда-нибудь текст из этого " + \
              f"текстового поля чтобы потом его туда вставить и нажать кнопку \"{translations_search['raw_request_button_text']['ru']}\". " + \
              "Тем самым вы избежите необходимости каждый раз выбирать поштучно нужные вам переводы и стихи."
    },
}