/////////////////////////////////////////////////////////////////////////////// Copyright (C) 1998 by Jorge Lodos// All rights reserved//// Distribute and use freely, except:// 1. Don't alter or remove this notice.// 2. Mark the changes you made//// Send bug reports, bug fixes, enhancements, requests, etc. to://    lodos@cigb.edu.cu/////////////////////////////////////////////////////////////////////////////// DIBStatic.cpp : implementation file//#define WINDOWS#include "stdafx.h"#include "CEyeDxDib.h"#include "CEyeDxDIBStatic.h"#ifdef _DEBUG#define new DEBUG_NEW#undef THIS_FILEstatic char THIS_FILE[] = __FILE__;#endif/////////////////////////////////////////////////////////////////////////////// CEyeDxDibStaticCEyeDxDibStatic::CEyeDxDibStatic(){}CEyeDxDibStatic::~CEyeDxDibStatic(){}BEGIN_MESSAGE_MAP(CEyeDxDibStatic, CStatic)	//{{AFX_MSG_MAP(CEyeDxDibStatic)	ON_WM_CTLCOLOR_REFLECT()	ON_WM_QUERYNEWPALETTE()	ON_WM_PALETTECHANGED()	//}}AFX_MSG_MAPEND_MESSAGE_MAP()BOOL CEyeDxDibStatic::LoadDib(LPCTSTR lpszFileName){	try	{		CFile file(lpszFileName, CFile::modeRead);		return LoadDib(file);	}	catch (CFileException* e)	{		e->Delete();		return FALSE;	}}BOOL CEyeDxDibStatic::LoadDib(CFile& file){	ASSERT_VALID(this);    	BOOL bResult = TRUE;			if (!m_DIB.Read(file))		bResult = FALSE;	DoRealizePalette(FALSE);	UpdateDib();	return bResult;}BOOL CEyeDxDibStatic::SetImageFromRaw24Bit(unsigned char *rawdata, long rows, long cols){	ASSERT_VALID(this);    	BOOL bResult = TRUE;			CRect PaintRect;	GetClientRect(&PaintRect);    	PaintRect.InflateRect(-1, -1);		if (!m_DIB.SetImageFromRaw24Bit(&PaintRect, rawdata, rows, cols))		bResult = FALSE;	DoRealizePalette(FALSE);			UpdateDib();		return bResult;}BOOL CEyeDxDibStatic::ZoomImageFromRaw24Bit(unsigned char *rawdata, long rows, long cols,											long dCols, long dRows, long dx, long dy){	ASSERT_VALID(this);    	BOOL bResult = TRUE;			CRect PaintRect;	GetClientRect(&PaintRect);    	PaintRect.InflateRect(-1, -1);		if (!m_DIB.ZoomImageFromRaw24Bit(&PaintRect, rawdata, rows, cols,									dCols, dRows, dx, dy))		bResult = FALSE;	DoRealizePalette(FALSE);			UpdateDib();		return bResult;}DWORD CEyeDxDibStatic::CopyBitmapData(CEyeDxDibStatic *obj){	ASSERT_VALID(this);    	BOOL bResult = TRUE;			CRect PaintRect;	GetClientRect(&PaintRect);    	PaintRect.InflateRect(-1, -1);		if (!m_DIB.CopyBitmapData(&PaintRect, obj->GetBitmapBits(), obj->GetBitmapInfo()))		bResult = FALSE;	DoRealizePalette(FALSE);			UpdateDib();		return bResult;}void CEyeDxDibStatic::ClearDib(){	ASSERT_VALID(this);		CClientDC dc(this);	CRect rectPaint;    	GetClientRect(&rectPaint);    	rectPaint.InflateRect(-1,-1);	    	CBrush* pBrushWhite;  	pBrushWhite = CBrush::FromHandle((HBRUSH)::GetStockObject(WHITE_BRUSH));    	dc.FillRect(&rectPaint, pBrushWhite);}void CEyeDxDibStatic::ResetImage(){	ASSERT_VALID(this);		CClientDC dc(this);	CRect rectPaint;    	GetClientRect(&rectPaint);    	rectPaint.InflateRect(-1,-1);	  	CBrush brush(RGB(192, 192, 192)); 	dc.FillRect(&rectPaint, &brush);	dc.SetTextColor(RGB(0, 0, 0));	dc.SetBkColor(RGB(192, 192, 192));		dc.DrawText("[None]", -1, &rectPaint, DT_SINGLELINE | DT_CENTER | DT_VCENTER);}// This routine takes position the position, radius, and RGB values for a// circle to draw. The values of rows and columns allow for scaling the// input x, y, and radius to the current view. Note that this draws the// circle in the view area - it is NOT drawn in the DIB image. Thus, if// the DIB is refreshed, the circles will disappear.void CEyeDxDibStatic::DrawCircle(long rows, long columns,						   double x, double y, double radius, 						   short penwidth,						   short red, short green, short blue){	CClientDC dc(this);	CRect rectPaint;    	GetClientRect(&rectPaint);    	long frame_height = rectPaint.Height();		long frame_width =  rectPaint.Width();		// Round all of these calculations up by adding 0.5 before truncation occurs	short theScaledX = (short)((x / (double) columns) * (double) frame_width + 0.5);		short theScaledY = (short)((y / (double) rows) * (double) frame_height + 0.5);		short theScaledHalfWidth = (short)((radius / (double) columns) * (double) frame_width + 0.5);		short theScaledHalfHeight = (short)((radius / (double) rows) * (double) frame_height + 0.5);		CRect theOval((short)(theScaledX - theScaledHalfWidth),						(short)(theScaledY - theScaledHalfHeight),						(short)(theScaledX + theScaledHalfWidth + 1),						(short)(theScaledY + theScaledHalfHeight + 1));							CPoint startAndEnd((short)(theScaledX - theScaledHalfWidth), 						(short)(theScaledY - theScaledHalfHeight));							CPen pen (PS_SOLID, penwidth, RGB(red, green, blue));	dc.SelectObject(&pen);	dc.Arc(theOval, startAndEnd, startAndEnd);}void CEyeDxDibStatic::PaintDib(BOOL bDibValid){	ASSERT_VALID(this);	//ClearDib();			CRect PaintRect;	GetClientRect(&PaintRect);    	PaintRect.InflateRect(-1, -1);	CClientDC dc(this);	if (bDibValid)	{		int nDestX, nDestY, nDestWidth, nDestHeight;		if (m_DIB.Width() < (DWORD)PaintRect.Width() && m_DIB.Height() < (DWORD)PaintRect.Height())		{ // If the image fits, just center it			nDestX = PaintRect.left + (PaintRect.Width() - m_DIB.Width())/2;			nDestY = PaintRect.top + (PaintRect.Height() - m_DIB.Height())/2;			nDestWidth = m_DIB.Height();			nDestHeight = m_DIB.Width();		}		else		{ // The bitmap doesn't fit, scale to fit 			if ((PaintRect.Width()/(float)m_DIB.Width()) <= (PaintRect.Height()/(float)m_DIB.Height()))			{ // Width is constraint				nDestWidth = PaintRect.Width();				nDestHeight = (nDestWidth*m_DIB.Height()) / m_DIB.Width();				nDestX = PaintRect.left;				nDestY = PaintRect.top + (PaintRect.Height() - nDestHeight) /2;			}			else			{ // Height is constraint						nDestHeight = PaintRect.Height();				nDestWidth = (nDestHeight*m_DIB.Width()) / m_DIB.Height();				nDestX = PaintRect.left + (PaintRect.Width() - nDestWidth) /2;				nDestY = PaintRect.top;			}		}		CRect RectDest(nDestX, nDestY, nDestX+nDestWidth, nDestY+nDestHeight);		CRect RectDib(0, 0, m_DIB.Width(), m_DIB.Height());		m_DIB.Paint(dc, &RectDest, &RectDib);     	}	else		ResetImage();			return;}void CEyeDxDibStatic::UpdateDib(){	ASSERT_VALID(this);	PaintDib(IsValidDib());}/////////////////////////////////////////////////////////////////////////////// CEyeDxDibStatic message handlersHBRUSH CEyeDxDibStatic::CtlColor(CDC* pDC, UINT nCtlColor) {	UpdateDib();	// TODO: Return a non-NULL brush if the parent's handler should not be called	return (HBRUSH)GetStockObject(NULL_BRUSH);}BOOL CEyeDxDibStatic::OnQueryNewPalette() {	return DoRealizePalette(FALSE);}void CEyeDxDibStatic::OnPaletteChanged(CWnd* pFocusWnd) {	DoRealizePalette(TRUE);}BOOL CEyeDxDibStatic::DoRealizePalette(BOOL bForceBackGround){	if (IsValidDib())	{		CClientDC dc(this);		if (!m_DIB.m_pPalette)			return FALSE;		HPALETTE hPal = (HPALETTE)m_DIB.m_pPalette->m_hObject;		HPALETTE hOldPalette = SelectPalette(dc, hPal, bForceBackGround);		UINT nChanged = dc.RealizePalette();		SelectPalette(dc, hOldPalette, TRUE);		if (nChanged == 0)	// no change to our mapping			return FALSE;				// some changes have been made; invalidate		UpdateDib();	}	return TRUE;}