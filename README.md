<h1 align="center">
  <a href="https://github.com/GhostPet/Mangapet">
    Mangapet
  </a>
</h1>

<div align="center">
  Will be used for implementing image protection techniques
</div>

<div align="center">
<br />

[![license](https://img.shields.io/github/license/GhostPet/Mangapet?style=flat-square)](LICENSE)
[![made with ♡ by GhostPet](https://img.shields.io/badge/made_with_%E2%99%A1_by-GhostPet-orange?style=flat-square)](https://github.com/GhostPet)

</div>

---

<details open="open">
<summary style="font-size:1.4rem;"><b style="font-size:1.5rem;margin-left:0.5rem">Table of Contents</b></summary>

- [About](#about)
- [Getting Started](#getting-started)
  - [Quick Start](#quick-start)
  - [Prerequisites](#prerequisites)
- [Roadmap](#roadmap)
- [License](#license)

</details>

---

## About

A manga website created for being used for implementing image protection techniques.
This is a modified repo of the [Create A Flask Blog - Flask Friday](https://youtube.com/playlist?list=PLCC34OHNcOtolz2Vd9ZSeSXWc8Bq23yEz&si=RXuNuItgTL_ntbHJ) by [Codemy.com](https://www.youtube.com/@Codemycom)

## Getting Started

### Quick Start
The recommended method to install **Manga Website** is by using [Git](https://git-scm.com/download)'s bash terminal.

To install them, you can copy and paste the code below line by line:
```sh
python -m venv your-virtual-env-name
source your-virtual-env-name/Scripts/activate

pip install -r requirements.txt
```

Then make sure you create an ".env" file and fill with your db information.

``` .env file
SQLALCHEMY_DATABASE_URI=
SECRET_KEY=
```

### Prerequisites

This web application requires these python libraries:

- **Flask** 3.0.2 - [Flask 3.0.x Docs](https://flask.palletsprojects.com/en/3.0.x/)

- **Flask-WTF** 1.2.1 - [Flask-WTF 1.2.x Docs](https://flask-wtf.readthedocs.io/en/1.2.x/)

- **Flask-SQLAlchemy** 3.1.1 - [Flask-SQLAlchemy 3.1.x Docs](https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/)

- **Flask-Migrate** 4.0.7 - [Flask-Migrate lastest Docs](https://flask-migrate.readthedocs.io/en/latest/)

- **Flask-Login** 0.6.3 - [Flask-Migrate 0.6.3 Docs](https://flask-login.readthedocs.io/en/0.6.3/)

- **cryptography** 42.0.5 - [cryptography 42.0.5 Docs](https://cryptography.io/en/42.0.5/)

- **Flask-CKEditor** 0.5.1 - [Flask-CKEditor lastest Docs](https://flask-ckeditor.readthedocs.io/en/latest/)

## Roadmap

See the [open issues](https://github.com/GhostPet/ImageWebsite/issues) for a list of proposed features (and known issues).

## License

This project is licensed under the **MIT license**. Feel free to edit and distribute this website as you like.

See [LICENSE](LICENSE) for more information.