import React, { Component } from 'react';


export default class Contour extends Component<{ contour: number[][][], onClick?:any, height: number, width: number, }> {

  render() {
    const { contour, height, width } = this.props;
    const { onClick } = this.props;

    const point_to_scale = (point: number[][]) => {
      let [x, y] = point[0];
      let x_ratio = window.innerWidth / width;
      let y_ratio = window.innerHeight / height;
      return [x * x_ratio, y * y_ratio];
    }

    const points: any = contour.map(point_to_scale).concat([point_to_scale(contour[0])]).map(point=> point.join(',')).join(' ');

    return (
      <polyline points={points} onClick={onClick} stroke='black' fill="white" strokeWidth={5} />
    );
  }

}