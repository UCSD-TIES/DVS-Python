// ===========================================================================//	CMFCMFCEyeDxLicenseFile.cp - based on UWindowState by  �1994 J. Rodden, DD/MF & Associates// ===========================================================================// Utilities for saving and restoring the EyeDx application's preferences.//// All rights reserved. You may use this code in any application, recognition// would be appreciated but is not required.#include <string.h>#include <stdio.h>#include <stdlib.h>#include "globals.h"#include "CMFCEyeDxLicenseFile.h"// ===========================================================================// This constructor is used to create the invisible license file as defined by the// specified FSSpec. This would be used for the backup file.// Use the alternative version that takes a filename to create the primary licenses file// in the Preferences folder.// This constructor is used to create the invisible license file inside the Preferences folder.// Use the alternative version that takes a FSSpec to create the backup licenses file.CMFCEyeDxLicenseFile::CMFCEyeDxLicenseFile(CString *inFileName){	// We make the file invisible}void CMFCEyeDxLicenseFile::SaveLicense(LicenseData *inLicenseData, short inResID){	// Make sure it's the current version		inLicenseData->version = kMISCVers1;		// -----------------------------------------	// Store the license data		LicenseData	**theHandle = 					(LicenseData**) ::Get1Resource( kLicenseData, inResID);		if ( theHandle != nil )		{		// a license resource already exists -- update it		**theHandle = *inLicenseData;	  ::ChangedResource(Handle(theHandle));	} 	else 	{		// no data has yet been saved -- add resource		theHandle = (LicenseData**) (NewHandle(sizeof(LicenseData)));		if ( theHandle != nil ) {			**theHandle = *inLicenseData;		  ::AddResource( Handle(theHandle), kLicenseData, inResID, nil);		}	}		if ( theHandle != nil ) 	{	  ::UpdateResFile(LPreferencesFile::GetResourceForkRefNum());	  ::ReleaseResource(Handle(theHandle));	}}// ===========================================================================voidCMFCEyeDxLicenseFile::LoadLicense(LicenseData *inLicenseData, short inResID){	LicenseData	theLicenseData;	LicenseData	**theHandle;		// -----------------------------------------	// Get saved license data			theHandle = (LicenseData**) ::Get1Resource(kLicenseData, inResID);			// Clear the structure and set defaults		memset(inLicenseData, 0, sizeof(LicenseData));		// Set the resource to invalid values so we can detect that no license exists		inLicenseData->version = kMISCVers1;	inLicenseData->expDate = 0L;				inLicenseData->lastUseDate = 0L;	inLicenseData->availableRuns = 0L;		inLicenseData->serialNumberLow = 0L;	inLicenseData->serialNumberHigh = 0L;	inLicenseData->checksum = 0L;			// -----------------------------------------	// Restore license	if ( theHandle != nil )		{	// handle to data succeeded -- retrieve saved user state		theLicenseData = **theHandle;		if (theLicenseData.version == kMISCVers1)			*inLicenseData = theLicenseData;			// Copy the structure		}}