<div align="center">
	<a  href="https://github.com/ClubInfoInsaT/take-a-guess">
		<img  src="https://raw.githubusercontent.com/ClubInfoInsaT/quizz/main/meta/logo-battle-royale-culture-g.png" width="600px" />
	</a>
</div>

<div align="center">
	<strong><i>Not a kahoot copy</i> - Club Info</strong>
</div>

<div align="center">I swear it's not a kahoot copy !!</div>
<br />
<div align="center">
  <a href="#">Site</a>
  <span> · </span>
  <a href="#">Documentation</a>
  <span> · </span>
  <a href="https://etud.insa-toulouse.fr/clubinfo/">Club Info</a>
</div>

<br />
<div align="center">
  <sub>Cooked by <a href="#">anonymous members of the club info</a> 👨‍🍳</sub>
</div>

---

## Installation

```console
npm install
```

## ⚠️ Important ⚠️

Eslint and Prettier are set up in the project to keep to code clean and readable
There is a [settings.json](.vscode/settings.json) for VSCode.

I hightly suggest you to install the following extensions from the marketplace:

- [Eslint](https://marketplace.visualstudio.com/items?itemName=dbaeumer.vscode-eslint)
- [Prettier](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode)
- [Vetur](https://marketplace.visualstudio.com/items?itemName=octref.vetur)

## 🔌 How to run the project 🔌

Here are the things to do to run the project

1. First open a terminal go to [backend](backend) and install the dependencies (Assuming you already have Python 3 and pip installed)

```console
cd backend
pip install -r requirements
```

2. Go back to the front-end side and install the depencies (Assuming you have node installed)

```console
npm install
```

3. Run the npm script `serve`

```console
npm run serve
```

4. Run the backend

```console
cd backend
python logic2.py
```

5. Open your favourite browser and open the url shown in the terminal. It should to something like this

```console
http://localhost:8080
```

> To create a room as an admin go to `http://localhost:8080/admin-home`
> To join a room as player got to `http://localhost:8080`

> The admin has to create the lobby **_BEFORE_** a player try to join the room

## 📔 How to run the project D-Day 📔

- Copy the http**s** link generated with the following command: `ngrok http 8000`
- Paste it here:
  ```javascript
  Vue.use(
    new VueSocketIO({
      debug: true,
      connection: "paste-link-here",
    })
  );
  ```
- Build the site with
  ```console
  npm run build-prod
  ```
- Send everything from [this directory](dist) to the server
- Start the python script

## Reports & Contributions

Feel free to open an issue to report any bugs or a pr to contribute.
Make sure to respect the [issue-template](.github/issue_template.md) and the [pr-templte](.github/pull_request_template.md)

Any pull request not formatted properly with eslint/prettier will not be reviewed

## Learn More

- You should have a look at [node](https://nodejs.org/en/) before
- To learn VueJS, check out the [Vue documention](https://vuejs.org/guide/introduction.html)
- [Vue Router](https://router.vuejs.org/)
- [Tailwindcss](https://tailwindcss.com/)
- [Typescript](https://www.typescriptlang.org/)
- Check out the [socket.io documention](https://socket.io/docs/v4/)

## Roadmap

- Turn the website into (react-native) app
