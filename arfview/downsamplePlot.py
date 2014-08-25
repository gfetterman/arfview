import pyqtgraph as pg
import numpy as np

class downsamplePlot(pg.PlotItem):
    def __init__(self, dataset, *args, **kwargs):
        super(downsamplePlot, self).__init__(*args, **kwargs)
        self.dataset = dataset
        self.data_item = pg.PlotDataItem()
        self.downsample()
        self.addItem(self.data_item)
        vb = self.getViewBox()
        vb.sigXRangeChanged.connect(self.downsample)
        #setting maximum view range (can only be used in version 9.9 of pyqtgraph)
        # max = np.max(dataset)
        # min = np.min(dataset)
        # maxYRange = 10 * (max - min)
        # vb.setLimits(yMax=max+maxYRange,yMin=min-maxYRange,
        #              maxYRange=maxYRange)
        
    def downsample(self):
        sr = float(self.dataset.attrs['sampling_rate'])
        t_min,t_max = self.getViewBox().viewRange()[0]
        t_min = max(0, t_min)
        t_max = min(self.dataset.len()/sr, t_max)
        i_min = int(t_min*sr)
        i_max = int(t_max*sr)
        npoints = i_max-i_min
        max_points=50000.0
        step=int(np.ceil(npoints/max_points))
        t = np.linspace(t_min, t_max, np.ceil(npoints/float(step)))
        if npoints>0:
                if len(self.dataset.shape) == 1:
                        self.data_item.setData(t, self.dataset[i_min:i_max:step])
                elif self.dataset.shape[0] >= self.dataset.shape[1]:
                        self.data_item.setData(t, self.dataset[i_min:i_max:step,0])
                else:
                        self.data_item.setData(t, self.dataset[0,i_min:i_max])
        else:
                self.data_item.clear()

