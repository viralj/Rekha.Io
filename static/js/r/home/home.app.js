class App extends React.Component {
    render() {
        return (
            React.createElement("div", {className: "container"}, 
                React.createElement("div", {className: "row"}, 
                    React.createElement("div", {className: "col s12 m12 l12"}, 
                        React.createElement("p", null, "Hello World!!!"), 
                        React.createElement("p", null, "This is test file!")
                    )
                )
            )
        );
    }
}


ReactDOM.render(React.createElement(App, null), document.getElementById('home-app'));