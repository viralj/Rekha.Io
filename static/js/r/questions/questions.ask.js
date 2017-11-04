class App extends React.Component {
    render() {
        return (
            React.createElement("div", {className: "container"}, 
                React.createElement("div", {className: "row"}), 
                React.createElement("div", {className: "row"}, 
                    React.createElement("div", {className: "col s12 m12 l12"}, 
                        React.createElement("div", {className: "row"}, 
                            React.createElement("div", {className: "col s12 m3 l3 col-content right"}, 
                                React.createElement("div", {className: "card"}, 
                                    React.createElement("div", {className: "card-content"}, 
                                        React.createElement("span", {className: "card-title"}, "Item"), 
                                        React.createElement("p", null, "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod" + ' ' +
                                            "tempor incididunt ut labore et dolore magna aliqua.")
                                    )
                                )
                            ), 
                            React.createElement("div", {className: "col s12 m9 l9 col-content"}, 
                                React.createElement("div", {className: "card"}, 
                                    React.createElement("div", {className: "card-content"}, 
                                        React.createElement("span", {className: "card-title"}, "Item"), 
                                        React.createElement("p", null, "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod" + ' ' +
                                            "tempor incididunt ut labore et dolore magna aliqua.")
                                    )
                                )
                            )
                        )
                    )
                )
            )
        );
    }
}


ReactDOM.render(React.createElement(App, null), document.getElementById('questions-ask-app'));