import app from "./src/app";

const server = app.listen(3001, () => {
    console.log("Running server...")
})

export default server;