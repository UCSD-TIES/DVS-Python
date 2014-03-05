#pragma once#include "globals.h"// This section defines the class used to describe variables. Note that the class varies// between Mac and Windows by using native data types, but the implementation of the// code is platform-specific. This allows common modules to access variables in a // portable manner.const long kCEyeDxVariableNameLength 	= 255;const long kCEyeDxVariableValueLength 	= 255;	// The value can be 255 charactersconst long kCEyeDxVariableDefaultLength = 63;const long kCEyeDxVariablePromptLength 	= 63;const long kCEyeDxVariableCommentLength = 63;const short	kNoExtraEntryLines 			= 0;			// 0 means just one line is displayedconst short kMaxExtraEntryLines 		= 3;		// Must match menu in the edit variable dialog!const short	kNoPromptOrder 				= -1;const short kNoExportOrder 				= -1;const long	kMaxVariablesPerDialog 		= 10;enum PromptStyle { kPromptOneAtATime = 0, kPromptAllInOne = 1 };#define kCheckBoxOnStr	(CommonStringLiteral_("Checked"))#define kCheckBoxOffStr	(CommonStringLiteral_("Unchecked"))#ifdef macintosh#include <TArray.h>#include <TArrayIterator.h>#include <LComparator.h>// This definition is for the Mac resource file, but we have to put it here so we don't have// a circular include file problem.// Note that the resource name is the variable name, and that the Value field in the// object is not saved. WARNING:the Resource Manager compares resource names ignoring// case! Thus, a variable named "VARIABLE" will be considered the same as "Variable". This// is not a problem as long as variable resources are not looked-up by name. This is the// case with the current design.struct CEyeDxVariablePrefs{	short	version;	short	extraEntryLines;	short	valueMustBeEntered;	short	varClass;	short	varType;	short	promptType;	short	dataType;	Str63	defaultValue;	Str63	promptString;	Str63	commentString;	short	hidden;	short	promptOrder;	short	exportOrder;	short	optionStrListID;		// On the Mac, this is a resource ID for a STR#	long	spare2;	long	spare3;	long	spare4;	long	spare5;	long	spare6;	Str255	value;					// Now we store the value as well in version 2};#pragma warn_hidevirtual off	template class TArray<CEyeDxShortStringType*>;#pragma warn_hidevirtual resettypedef	TArray<CEyeDxShortStringType*> CTemplateShortStrArray;class	CCEyeDxLongStringTypeComparator : public LComparator {public:								CCEyeDxLongStringTypeComparator();	virtual						~CCEyeDxLongStringTypeComparator();				virtual SInt32				Compare(									const void*			inItemOne,									const void* 		inItemTwo,									UInt32				inSizeOne,									UInt32				inSizeTwo) const;									virtual Boolean				IsEqualTo(									const void*			inItemOne,									const void* 		inItemTwo,									UInt32				inSizeOne,									UInt32				inSizeTwo) const;									virtual LComparator*		Clone();									static CCEyeDxLongStringTypeComparator*	GetComparator();	protected:	static CCEyeDxLongStringTypeComparator*	sCCEyeDxLongStringTypeComparator;};#else // Windows Definitions#include <afxtempl.h>// This definition is for the Windows resource file, but we have to put it here so we don't have// a circular include file problem.const int	kEyeDxVariableWinNameStrOffset		= 0;	// The name string is always the firstconst int	kEyeDxVariableWinDefaultStrOffset	= 1;	// Add this to the name string ID to get the Default IDconst int	kEyeDxVariableWinPromptStrOffset	= 2;	// Add this to the name string ID to get the prompt IDconst int	kEyeDxVariableWinCommentStrOffset	= 3;	// Add this to the name string ID to get the comment IDconst int	kEyeDxVariableWinOptionsStrOffset	= 4;	// This defines an individual structure of the array of resources that define the EyeDx-provided variables.// When fetched, the application will retrieve an array of these, with the last entry have 0 as the nameStrID// value. Note that this structure is NOT used for storage of variables between invocations of the program (that's// handled by serialization). Rather, this is just a way to define default variables within the application file// for distribution.struct CEyeDxVariablePrefs{	short	nameStrID;				// The ID for the variable name (must exist or be 0 to indicate the last entry!)	short	version;	short	extraEntryLines;	short	valueMustBeEntered;	short	varClass;	short	varType;	short	promptType;	short	dataType;	short	hidden;	short	promptOrder;	short	exportOrder;	short	numOptionStrs;			// Since Windows doesn't have the equivalent of a STR# resource,									// the numOptionStrs is a count of the strings, and the value of									// kEyeDxVariableWinOptionsStrOffset added to the resource ID is									// the ID of the first string in the list. The other strings must be									// in consecutive order following this first string ID	short	spare2;	short	spare3;	short	spare4;	short	spare5;	short	spare6;};typedef	CTypedPtrArray<CPtrArray, CEyeDxShortStringType*> CTemplateShortStrArray;enum sortOrder { kSortColumnByName = 0, 				   kSortColumnByClass = 1,				   kSortColumnByType = 2,				   kSortColumnByDataType = 3,				   kSortColumnByOtherAttributes = 4 };#endif// Now we declare the class based on the platform#ifdef macintoshclass CEyeDxVariable{#elseconst int kCEyeDxVariableCurrentSchema = 1;class CEyeDxVariable : public CObject{	DECLARE_SERIAL(CEyeDxVariable)#endifpublic:		enum VariableClass 	{ kEyeDx = 0, kUser = 1 };	enum VariableType 	{ kFixed = 0, kPrompted = 1, kCalculated = 2 };	enum PromptType 	{ kPromptNone = -1, kPromptOnStart = 0, kPromptForSubject = 1, 						  kPromptForSession = 2, kPromptForEndOfSession = 3, 						  kPromptDisabled = 4,						  kPromptTypeLast = kPromptDisabled };	// Note that all calculated variables should have their DataType set properly in the template resource	// so that the ResetValue() routine will work properly.		enum DataType 			{ kTypeNone = -1, kGeneralString = 0, kDate = 1,							  kTime = 2, kIntegerNumber = 3, kPastDate = 4, 							  kFloatNumber = 5, kCheckBox = 6, kMenu = 7 };	// Constructors								// Must have a default constructor for serialization															CEyeDxVariable();														CEyeDxVariable(CEyeDxVariable::VariableClass theClass);														CEyeDxVariable(const CEyeDxVariable &srcVariable);							CEyeDxVariable(CEyeDxLongStringType *theName, CEyeDxVariablePrefs *srcVariablePrefs);							// Constructor for a Fixed Type variable														CEyeDxVariable(VariableClass theClass,								 CEyeDxLongStringType theName,								 CEyeDxLongStringType theValue,								 CEyeDxShortStringType theCommentString = EMPTYSTR,								 short theExportOrder = kNoExportOrder);								 							// Constructor for a Prompted Type variable														CEyeDxVariable(VariableClass theClass,								 CEyeDxLongStringType theName,								 CEyeDxShortStringType thePromptString,								 PromptType thePromptType = kPromptForSubject,								 DataType theDataType = kGeneralString,								 CEyeDxBooleanType theValueMustBeEntered = false,								 CEyeDxShortStringType theDefaultValue = EMPTYSTR,								 CEyeDxShortStringType theCommentSTring = EMPTYSTR,								 short thePromptOrder = kNoPromptOrder,								 short theExportOrder = kNoExportOrder,								 short theExtraEntryLines = kNoExtraEntryLines);			// Destructor								~CEyeDxVariable();		CEyeDxVariable&			operator=(const CEyeDxVariable &srcVariable);	#ifndef macintosh	void					Serialize(CArchive &);		static int CALLBACK  	CompareFunc(LPARAM lParam1, LPARAM lParam2, LPARAM lParamSort);#endif	// Accessor member functions		void					SetVariableClass(VariableClass newVariableClass) { mVariableClass = newVariableClass; };	void					SetVariableType(VariableType newVariableType) { mVariableType = newVariableType; };	void					SetWhenToPrompt(PromptType whenToPrompt) { mPromptType = whenToPrompt; };	void					SetDataType(DataType validateVarType) { mDataType = validateVarType; };	void					SetPromptOrder(short promptOrder) { mPromptOrder = promptOrder; };	void					SetExportOrder(short exportOrder) { mExportOrder = exportOrder; };	void					SetValueMustBeEntered(CEyeDxBooleanType theValueMustBeEntered) { mValueMustBeEntered = theValueMustBeEntered; };	void					SetVariableIsHidden(CEyeDxBooleanType theIsHidden) { mIsHidden = theIsHidden; };	void					SetExtraEntryLines(short theExtraEntryLines) { mExtraEntryLines = theExtraEntryLines; };		void					SetName(CEyeDxLongStringType newName) { mName = newName; };	void					SetDefaultValue(CEyeDxLongStringType newDefaultValue) { mDefaultValue = newDefaultValue; mValue = newDefaultValue; };	void					SetDefaultValue(const char *newDefaultValue) { mDefaultValue = newDefaultValue; mValue = newDefaultValue; };#ifdef macintosh	void					SetDefaultValue(long newDefaultValue) { mDefaultValue = newDefaultValue; mValue = mDefaultValue; };#else	void					SetDefaultValue(long newDefaultValue) { mDefaultValue.Format("%d", newDefaultValue); mValue = mDefaultValue; };#endif	void					SetValue(CEyeDxLongStringType newValue) { mValue = newValue; };	void					SetValue(DCTime timeValue);	void					SetValue(const char *newValue) { mValue = newValue; };#ifdef macintosh	void					SetValue(long newValue) { mValue = newValue; };#else	void					SetValue(long newValue) { mValue.Format("%d", newValue); };#endif	void					SetValueToDefault() { mValue = mDefaultValue; };	void					ResetValue();	// Sets the value to a reasonable value for the type ("0" for integers, current time, current date, etc.)	void					SetPromptString(CEyeDxShortStringType newPromptString) { mPromptString = newPromptString; };	void					SetCommentString(CEyeDxShortStringType newCommentString) { mCommentString = newCommentString; };	VariableClass			GetVariableClass() { return mVariableClass; };	VariableType			GetVariableType() { return mVariableType; };	PromptType				GetWhenToPrompt() { return mPromptType; };	DataType				GetDataType() { return mDataType; };	short					GetPromptOrder() { return mPromptOrder; };	short					GetExportOrder() { return mExportOrder; };	CEyeDxBooleanType		GetValueMustBeEntered() { return mValueMustBeEntered; };	CEyeDxBooleanType		GetVariableIsHidden() { return mIsHidden; };	short					GetExtraEntryLines() { return mExtraEntryLines; };		CEyeDxLongStringType	*GetName() { return &mName; };	CEyeDxShortStringType	*GetDefaultValue() { return &mDefaultValue; };	CEyeDxLongStringType	*GetValue() { return &mValue; };#ifdef macintosh	void					GetValue(long &theValue) { theValue = SInt32(mValue); };	void					GetValue(short &theValue) { theValue = (short)SInt32(mValue); };#else	void					GetValue(long &theValue) { theValue = strtol(mValue, NULL, 10); };	void					GetValue(short &theValue) { theValue = (short)strtol(mValue, NULL, 10); };#endif	CEyeDxShortStringType	*GetPromptString() { return &mPromptString; };	CEyeDxShortStringType	*GetCommentString() { return &mCommentString; };		CTemplateShortStrArray	*GetOptionStringsArray() { return mOptionStrings; };		void					ValidateDefault();	protected:	void					Init(CEyeDxVariable::VariableClass theClass,								 CEyeDxVariable::VariableType theType,								 CEyeDxLongStringType theName,								 CEyeDxShortStringType thePromptString,								 CEyeDxVariable::PromptType thePromptType,								 CEyeDxVariable::DataType theDataType,								 CEyeDxBooleanType theValueMustBeEntered,								 CEyeDxShortStringType theDefaultValue,								 CEyeDxShortStringType theCommentString,								 short thePromptOrder,								 short theExportOrder,								 short theExtraEntryLines,								 CEyeDxBooleanType theIsHidden,								 CTemplateShortStrArray *theOptionsList = NULL);private:		CEyeDxLongStringType	mName;	// Must be LStr255 to match length of resource names	VariableClass			mVariableClass;	VariableType			mVariableType;	PromptType				mPromptType;	DataType				mDataType;	CEyeDxShortStringType	mDefaultValue;	CEyeDxLongStringType	mValue;	CEyeDxShortStringType	mPromptString;	CEyeDxShortStringType	mCommentString;	short					mPromptOrder;	short					mExportOrder;	CEyeDxBooleanType		mValueMustBeEntered;	CEyeDxBooleanType		mIsHidden;	short					mExtraEntryLines;	CTemplateShortStrArray	*mOptionStrings;	// Used only if the variable is a menu type};#ifdef macintosh// ΡΡΡΡΡΡΡΡΡΡΡΡΡΡΡΡΡΡΡΡΡΡΡΡΡΡΡΡΡΡΡΡΡΡΡΡΡΡΡΡΡΡΡΡΡΡΡΡΡΡΡΡΡΡΡΡΡΡΡΡΡΡΡΡΡΡΡΡΡΡΡΡΡΡΡclass	CEyeDxVariableNameComparator : public LComparator {public:								CEyeDxVariableNameComparator();	virtual						~CEyeDxVariableNameComparator();				virtual SInt32				Compare(									const void*			inItemOne,									const void* 		inItemTwo,									UInt32				inSizeOne,									UInt32				inSizeTwo) const;									virtual Boolean				IsEqualTo(									const void*			inItemOne,									const void* 		inItemTwo,									UInt32				inSizeOne,									UInt32				inSizeTwo) const;									virtual LComparator*		Clone();									static CEyeDxVariableNameComparator*	GetComparator();	protected:	static CEyeDxVariableNameComparator*	sCEyeDxVariableNameComparator;};class	CEyeDxVariablePromptComparator : public LComparator {public:								CEyeDxVariablePromptComparator();	virtual						~CEyeDxVariablePromptComparator();				virtual SInt32				Compare(									const void*			inItemOne,									const void* 		inItemTwo,									UInt32				inSizeOne,									UInt32				inSizeTwo) const;									virtual Boolean				IsEqualTo(									const void*			inItemOne,									const void* 		inItemTwo,									UInt32				inSizeOne,									UInt32				inSizeTwo) const;									virtual LComparator*		Clone();									static CEyeDxVariablePromptComparator*	GetComparator();	protected:	static CEyeDxVariablePromptComparator*	sCEyeDxVariablePromptComparator;};class	CEyeDxVariableExportComparator : public LComparator {public:								CEyeDxVariableExportComparator();	virtual						~CEyeDxVariableExportComparator();				virtual SInt32				Compare(									const void*			inItemOne,									const void* 		inItemTwo,									UInt32				inSizeOne,									UInt32				inSizeTwo) const;									virtual Boolean				IsEqualTo(									const void*			inItemOne,									const void* 		inItemTwo,									UInt32				inSizeOne,									UInt32				inSizeTwo) const;									virtual LComparator*		Clone();									static CEyeDxVariableExportComparator*	GetComparator();	protected:	static CEyeDxVariableExportComparator*	sCEyeDxVariableExportComparator;};class	CEyeDxVariableClassComparator : public LComparator {public:								CEyeDxVariableClassComparator();	virtual						~CEyeDxVariableClassComparator();				virtual SInt32				Compare(									const void*			inItemOne,									const void* 		inItemTwo,									UInt32				inSizeOne,									UInt32				inSizeTwo) const;									virtual Boolean				IsEqualTo(									const void*			inItemOne,									const void* 		inItemTwo,									UInt32				inSizeOne,									UInt32				inSizeTwo) const;									virtual LComparator*		Clone();									static CEyeDxVariableClassComparator*	GetComparator();	protected:	static CEyeDxVariableClassComparator*	sCEyeDxVariableClassComparator;};class	CEyeDxVariableTypeComparator : public LComparator {public:								CEyeDxVariableTypeComparator();	virtual						~CEyeDxVariableTypeComparator();				virtual SInt32				Compare(									const void*			inItemOne,									const void* 		inItemTwo,									UInt32				inSizeOne,									UInt32				inSizeTwo) const;									virtual Boolean				IsEqualTo(									const void*			inItemOne,									const void* 		inItemTwo,									UInt32				inSizeOne,									UInt32				inSizeTwo) const;									virtual LComparator*		Clone();									static CEyeDxVariableTypeComparator*	GetComparator();	protected:	static CEyeDxVariableTypeComparator*	sCEyeDxVariableTypeComparator;};class	CEyeDxVariableDataTypeComparator : public LComparator {public:								CEyeDxVariableDataTypeComparator();	virtual						~CEyeDxVariableDataTypeComparator();				virtual SInt32				Compare(									const void*			inItemOne,									const void* 		inItemTwo,									UInt32				inSizeOne,									UInt32				inSizeTwo) const;									virtual Boolean				IsEqualTo(									const void*			inItemOne,									const void* 		inItemTwo,									UInt32				inSizeOne,									UInt32				inSizeTwo) const;									virtual LComparator*		Clone();									static CEyeDxVariableDataTypeComparator*	GetComparator();	protected:	static CEyeDxVariableDataTypeComparator*	sCEyeDxVariableDataTypeComparator;};#pragma warn_hidevirtual off	class CEyeDxVariable;	template class TArray<CEyeDxVariable*>;#pragma warn_hidevirtual reset#define	CEyeDxTemplateVariableArray	TArray<CEyeDxVariable*>#else#define	CEyeDxTemplateVariableArray	CTypedPtrArray<CPtrArray, CEyeDxVariable*>#endif// Now declare the class based onthe platform#ifdef macintoshclass CEyeDxVariableList{#elseconst int kCEyeDxVariableListCurrentSchema = 1;class CEyeDxVariableList : public CObject{	DECLARE_SERIAL(CEyeDxVariableList)#endifpublic:	enum						SortOrder { kSortByName = 0, kSortByPromptOrder = 1, kSortByExportOrder = 2, kSortByClass = 3, kSortByType = 4, kSortByDataType = 5  };								// Must have a default constructor for serialization																CEyeDxVariableList();								// Default is to sort by name																								CEyeDxVariableList(CEyeDxVariableList::SortOrder sortOrder);							virtual						~CEyeDxVariableList();	#ifndef macintosh	void						Serialize(CArchive &);	#endif	CEyeDxBooleanType			VariableExists(CEyeDxLongStringType Name);		void						AddVariable(CEyeDxVariable *theVariable);		void						InsertVariableAt(CEyeDxArrayIndexType inIndexA, CEyeDxVariable *theVariable);		void						DeleteVariable(CEyeDxVariable *theVariable);		void						DeleteVariableByName(CEyeDxLongStringType Name);		void						DeleteVariableByIndex(CEyeDxArrayIndexType Index);		CEyeDxVariable				*GetVariableByName(CEyeDxLongStringType Name);		CEyeDxVariable				*GetVariableByIndex(CEyeDxArrayIndexType Index);		void						SetAllVariablesToDefault(CEyeDxVariable::VariableType theType,														 CEyeDxVariable::PromptType thePromptType);														 	CEyeDxVariable				*GetNextPromptedVariable(CEyeDxVariable::PromptType promptType, short theAfterPromptOrder);	short						GetNextAvailablePromptNumber(CEyeDxVariable::PromptType promptType);		void						CompressPromptOrder();		CEyeDxVariable				*GetNextExportedVariable(short theAfterExportOrder);	void						CompressExportOrder();		unsigned long				GetCount();	#ifdef macintosh	LComparator 				*GetComparator(SortOrder theSortOrder);		SortOrder					GetSortOrder() { return mSortOrder; };		void						SetSortOrder(SortOrder);											  	void						Sort() { mVariableList->Sort(); };		void						SwapItems(CEyeDxArrayIndexType inIndexA,	CEyeDxArrayIndexType inIndexB) { mVariableList->SwapItems(inIndexA, inIndexB); };	void						SetKeepSorted(CEyeDxBooleanType keepSorted) { mVariableList->SetKeepSorted(keepSorted); };#else	void						SwapItems(CEyeDxArrayIndexType inIndexA,	CEyeDxArrayIndexType inIndexB)								{									CEyeDxVariable *varA = mVariableList->GetAt(inIndexA);									mVariableList->SetAt(inIndexA, mVariableList->GetAt(inIndexB));									mVariableList->SetAt(inIndexB, varA);																	};	void						SetKeepSorted(CEyeDxBooleanType keepSorted) { mKeepSorted = keepSorted; };#endifprivate:	CEyeDxTemplateVariableArray	*mVariableList;	SortOrder					mSortOrder;#ifdef macintosh		LComparator					*mComparator;	LComparator					*mNameComparator;	LComparator					*mPromptOrderComparator;	LComparator					*mExportOrderComparator;	LComparator					*mClassComparator;	LComparator					*mTypeComparator;	LComparator					*mDataTypeComparator;#else	CEyeDxBooleanType			mKeepSorted;	// Under Windows we have to do sorting ourselves#endif};