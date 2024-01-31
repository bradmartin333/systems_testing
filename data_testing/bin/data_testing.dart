import 'dart:math';

import 'package:iirjdart/butterworth.dart';
import 'package:raylib/raylib.dart';
import 'package:data_testing/window_utils.dart';

void main() {
  int idx = 0;
  int maxIdx = 5000;
  Random rng = Random();

  List<double> dataToFilter = [];
  for (var i = 0; i < maxIdx; i++) {
    dataToFilter.add(rng.nextDouble());
  }

  Butterworth butterworth = Butterworth();
  butterworth.lowPass(4, 250, 50);

  List<double> filteredData = [];
  for (var v in dataToFilter) {
    filteredData.add(butterworth.filter(v));
  }

  initLibrary(
    windows: 'F:/vcpkg/packages/raylib_x64-windows/bin/raylib.dll',
  );

  WindowState ws = WindowState();
  ws.linePlots = [
    LinePlot(Rectangle(10, 200, ws.wid - 20, 100), Color.blue, Color.white),
    LinePlot(Rectangle(10, 300, ws.wid - 20, 100), Color.pink, Color.white),
  ];

  initWindow(
    ws.wid,
    ws.hgt,
    'dart-raylib',
  );

  setTargetFPS(60);

  while (!windowShouldClose()) {
    ws.update();

    ws.linePlots.first.sendValue(dataToFilter[idx]);
    ws.linePlots.last.sendValue(filteredData[idx]);
    idx++;
    if (idx > maxIdx) {
      idx = 0;
    }

    beginDrawing();
    clearBackground(Color.white);
    ws.drawAllLinePlots();
    endDrawing();
  }

  closeWindow();
}
