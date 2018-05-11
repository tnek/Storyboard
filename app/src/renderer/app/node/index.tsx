import React, { Component } from 'react';

class Node extends Component<{tag: string, x: number, y: number, height: number, width: number, parent: any, children?: any[], x_ratio: number, y_ratio: number}> {

  render() {
    const { tag, x, y, height, width, children } = this.props;
    const { x_ratio, y_ratio } = this.props;
    const { x: parent_x, y: parent_y } = this.props.parent;

    const element: any = React.createElement(
      tag,
      {
        style: {
          position: 'absolute',
          top: (y - height - parent_y) * y_ratio,
          left: (x - parent_x) * x_ratio,
          height: height * y_ratio,
          width: width * x_ratio,
          border: '1px solid black',
          backgroundColor: "hsla(" + Math.random() * 360 + ", 100%, 75%, 0.2)",
          borderRadius: '1px',
        },
      },
      children && children.map((child:any, index: number) =>
        <Node
          key={index}
          {...child}
          parent={{
            x: x - parent_x,
            y: y - height - parent_y,
          }}
          x_ratio={x_ratio}
          y_ratio={y_ratio}
        />
      ),
    );

    return element;
  }
}



export default Node;