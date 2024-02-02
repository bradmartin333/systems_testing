# Run example app outside download directory
1. Install VS2022 Desktop development for C++ defaults + MFC option
1. [Download SDK from Lumix](https://av.jpn.support.panasonic.com/support/global/cs/soft/tool/sdk.html)
1. In VS2022, create new `Project from existing code` and use the `LumixRemoteControlLibraryBeta1.00\TetherSDKSample\LiveView01` directory
	- Check box for MFC
1. Right click on solution and select properties
	- Linker -> General -> add lib dirs to Additional Library Directories
	- Linker -> Input -> add `Lmxptpif.lib` to Additional Dependencies
1. The necessary bugfixes for the Win10 upgade are in this repo (The `devInfo.find_PnpDevice_Info[i].dev_ModelName` issue)

# Next steps
- Use the library with cross platform GUI instead of MFC