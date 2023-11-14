<template>
    <h1>Tic tac toe</h1>
    <div id="tictac">
        <table v-if="1==1">
            <tr class="top">
                <td class="first"><br></td>
                <td><br></td>
                <td class="last"><br></td>
            </tr>
            <tr>
                <td class="first"><br></td>
                <td><br></td>
                <td class="last"><br></td>
            </tr>
            <tr class="footer">
                <td class="first"><br></td>
                <td><br></td>
                <td class="last"><br></td>
            </tr>
        </table>
        <div v-else>
            <p>Press the button to start playing</p>
            <button v-bind="pressed">Start playing!</button>
        </div>
    </div>
</template>

<script>
export default {
    name: 'TicTacToe',
    props: {
        pressed: String
    }
}
</script>

<style scoped>
    * {
        font-size: 10vh;
    }
    table {
        min-height: 100vh;
        border-collapse: collapse;
        margin:auto;
    }
    body {
        min-height: 100vh;
    }
    tr {
        min-height: 33vh;
        border-bottom: solid 20px;
    }
    td, th{
        min-width: 30vw;
        min-height: 30vh;
        border-right: solid 20px;
        border-left: solid 20px;
    }
    th {
        border-right: solid 2px;
    }
    .last {
        border-right: none;
    }
    .first{
        border-left: none;
    }
    .footer {
        border-bottom: none;
    }
    .top {
        border-top:none;
    }
</style>
