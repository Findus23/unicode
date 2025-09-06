import { mount } from "svelte"
import "./app.scss"
import App from "./App.svelte"

// import "../node_modules/bootstrap/scss/bootstrap.scss"

const app = mount(App, {
    target: document.getElementById("app")!
})

export default app
