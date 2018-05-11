import React, { Component } from 'react';

import Contour from './contour';
import Node from './node';

// export default class Root extends Component<{contours?: number[][][][], height: number, width: number}>{
//
//   render() {
//
//     const { height, width } = this.props;
//     const contours = this.props.contours || [
//       [[[0, 0]], [[50, 50]], [[0, 50]], [[0, 0]]],
//       [[[0, 0]], [[50, 0]], [[50, 50]], [[0, 0]]]
//     ];
//     return (
//       <div id="root">
//         <svg width={window.innerWidth} height={window.innerHeight}>
//           {contours.map((contour: any, index: number) =>
//             <Contour contour={contour} key={index} onClick={()=>console.log('Clicked', index)} height={height} width={width} />
//           )}
//         </svg>
//         {/* <Contour contour={[[[0, 0]], [[50, 50]], [[0, 50]], [[0, 0]]]} index={1} />
//         <Contour contour={[[[0, 0]], [[50, 0]], [[50, 50]], [[0, 0]]]} index={2} /> */}
//       </div>
//     );
//   }
// }

export default class Root extends Component<{data: any, x_ratio: number, y_ratio: number}> {

  render() {
    const { data, x_ratio, y_ratio } = this.props;
    console.log('root');
    console.log(data);
    return (
      <div id="root">
        <Node {...data} x_ratio={x_ratio} y_ratio={y_ratio} />
      </div>
    );
  }
}