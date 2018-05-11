import React from 'react';
import { render } from 'react-dom';

import fs from 'fs';

import App from './app';

const data = require('common/data.json');

// const data = {
//   tag: 'div',
//   x: 0,
//   y: 0,
//   height: 20,
//   width: 20,
//   children: [
//     {
//       tag: 'div',
//       x: 50,
//       y: 50,
//       height: 30,
//       width: 30,
//       children: [
//         {
//           tag: 'div',
//           x: 150,
//           y: 50,
//           height: 20,
//           width: 20,
//         },
//       ],
//     }
//   ],
//   parent: {
//     x: 0,
//     y: 0,
//   }
// };

const x_ratio =  window.innerWidth / data.width;
const y_ratio = window.innerHeight / data.height;


render(
  <App data={...data}
  x_ratio={x_ratio}
  y_ratio={y_ratio}
  />,
  document.getElementById('app')
);